import machine
import asyncio
import sys
import utime


class Motors:
    def __init__(self, orientation_lock, drone_orientation, motor_lock):
        self.ESC_FREQUENCY = 50
        self.MIN_THROTTLE = 1000  # 1000 # us
        self.MAX_THROTTLE = 1200  # Set to for safety for now #2000 # us
        self.ESC_ARM_TIME = 2  # seconds
        self.is_armed = False  # Boolean representing if the drone is armed.
        # PWM for each motor
        self.pwm_fl = None  # Front Left Motor PWM
        self.pwm_fr = None  # Front Right Motor PWM
        self.pwm_bl = None  # Back Left Motor PWM
        self.pwm_br = None  # Back Right Motor PWM
        # Throttle (decimal representation [0-1]) for each motor.
        self.throttle_fl = 0
        self.throttle_fr = 0
        self.throttle_bl = 0
        self.throttle_br = 0
        self.pitch_kp = 0.00043714285
        self.pitch_ki = 0.00255
        self.pitch_kd = 0.00002571429
        self.roll_kp = 0.00043714285
        self.roll_ki = 0.00255
        self.roll_kd = 0.00002571429
        self.yaw_kp = 0.001714287
        self.yaw_ki = 0.003428571
        self.yaw_kd = 0
        self.poll_frequency = (
            250  # Target Poll Frequency to update motor thrust values in Hz.
        )
        self.quit = False
        self.orientation_lock = orientation_lock
        self.drone_orientation = drone_orientation
        self.motor_lock = motor_lock

    def run(self, pwm_fl_pin, pwm_fr_pin, pwm_bl_pin, pwm_br_pin):
        self.pwm_fl = machine.PWM(machine.Pin(pwm_fl_pin))
        self.pwm_fr = machine.PWM(machine.Pin(pwm_fr_pin))
        self.pwm_bl = machine.PWM(machine.Pin(pwm_bl_pin))
        self.pwm_br = machine.PWM(machine.Pin(pwm_br_pin))

        # Variables used to calculate PID Feedback Loops
        prev_time = utime.ticks_ms() - 4
        roll_last_integral = 0
        pitch_last_integral = 0
        yaw_last_integral = 0
        roll_last_error = 0
        pitch_last_error = 0
        yaw_last_error = 0

        self.arm()

        # Motor Control Loop
        try:
            while not self.quit:
                curr_time = utime.ticks_ms()
                dt = (curr_time - prev_time) / 1000
                # Desired Throttle
                target_throttle = 0.2

                # Desired Orientation (Roll, Pitch, Yaw)
                input_roll = 0
                input_pitch = 0
                input_yaw = 0

                # Grab Current Orientation (Roll, Pitch, Yaw)
                self.orientation_lock.acquire()
                current_roll = self.drone_orientation.roll
                current_pitch = self.drone_orientation.pitch
                current_yaw = self.drone_orientation.yaw
                self.orientation_lock.release()

                # Calculate Error - difference between actual and desired
                roll_error_rate = input_roll - current_roll
                pitch_error_rate = input_pitch - current_pitch
                yaw_error_rate = input_yaw - current_yaw

                # Roll PID Calculation
                roll_p = roll_error_rate * self.roll_kp
                roll_i = roll_last_integral + (roll_error_rate * self.roll_ki * dt)
                roll_d = self.roll_kd * (roll_error_rate - roll_last_error) / dt
                roll_last_error = roll_error_rate
                roll_last_integral = roll_i
                roll_pid = roll_p + roll_i + roll_d

                # Pitch PID Calculation
                pitch_p = pitch_error_rate * self.pitch_kp
                pitch_i = pitch_last_integral + (pitch_error_rate * self.pitch_ki * dt)
                pitch_d = self.pitch_kd * (pitch_error_rate - pitch_last_error) / dt
                pitch_last_error = pitch_error_rate
                pitch_last_integral = pitch_i
                pitch_pid = pitch_p + pitch_i + pitch_d

                # Yaw PID Calculation
                yaw_p = yaw_error_rate * self.yaw_kp
                yaw_i = yaw_last_integral + (yaw_error_rate * self.yaw_ki * dt)
                yaw_d = self.yaw_kd * (yaw_error_rate - yaw_last_error) / dt
                yaw_last_error = yaw_error_rate
                yaw_last_integral = yaw_i
                yaw_pid = yaw_p + yaw_i + yaw_d

                # Set throttle Values
                t1 = target_throttle + pitch_pid + roll_pid - yaw_pid  # Front Right
                t2 = target_throttle + pitch_pid - roll_pid + yaw_pid  # Back Right
                t3 = target_throttle - pitch_pid + roll_pid + yaw_pid  # Front Left
                t4 = target_throttle - pitch_pid - roll_pid - yaw_pid  # Back Left
                self.set_throttle(t3, t1, t4, t2)
                # print("[LOG] SET THROTTLE", t3, t1, t4, t2, dt, end="\r")

                # Wait for correct time to make Hz the target poll frequency
                prev_time = curr_time
                elapsed_time = utime.ticks_ms() - curr_time
                if (elapsed_time / 1000) < (1 / self.poll_frequency):
                    utime.sleep((1 / self.poll_frequency) - (elapsed_time / 1000))

        except Exception as e:
            print("[ERROR]: The following traceback was found:")
            print("-----------------------------------------------")
            sys.print_exception(e)
            print("-----------------------------------------------")
        except KeyboardInterrupt as e:
            print("[KEYBOARD INTERRUPT]: In Motors -  Manually Stopping")
            print("-----------------------------------------------")
            sys.print_exception(e)
            print("-----------------------------------------------")

        quit_flag = True
        self.disarm()
        print("[TERMINATION] Motors Coroutine")

    def close(self):
        self.quit = True

    def set_pid(pitch, roll, yaw):
        if not self.is_armed:
            self.pitch_p = pitch["p"]
            self.pitch_i = pitch["i"]
            self.pitch_d = pitch["d"]
            self.roll_p = roll["p"]
            self.roll_i = roll["i"]
            self.roll_d = roll["d"]
            self.yaw_p = yaw["p"]
            self.yaw_i = yaw["i"]
            self.yaw_d = yaw["d"]
            print("[LOG] PID parameters Updated!")
        else:
            print("[LOG] Cannot change PID parameters while Drone is Armed!")

    def set_throttle(self, throttle_fl, throttle_fr, throttle_bl, throttle_br):
        # Input:
        # throttle_XX - float representing the throttle as a decimal (0-1).
        # ---------------------------------------------------------------------
        # Check if throttles are in range.
        if throttle_fl > 1:
            throttle_fl = 1
        elif throttle_fl < 0:
            throttle_fl = 0
        if throttle_fr > 1:
            throttle_fr = 1
        elif throttle_fr < 0:
            throttle_fr = 0
        if throttle_bl > 1:
            throttle_bl = 1
        elif throttle_bl < 0:
            throttle_bl = 0
        if throttle_br > 1:
            throttle_br = 1
        elif throttle_br < 0:
            throttle_br = 0
        # print("[LOG] SET THROTTLE", throttle_fl, throttle_fr, throttle_bl, throttle_br, end="\r")
        # Set motors to throttle values.
        self.throttle_fl = throttle_fl
        self.pwm_fl.duty_ns(
            (
                int(
                    throttle_fl * (self.MAX_THROTTLE - self.MIN_THROTTLE)
                    + self.MIN_THROTTLE
                )
                * 1000
            )
        )

        self.throttle_fr = throttle_fr
        self.pwm_fr.duty_ns(
            int(
                (
                    throttle_fr * (self.MAX_THROTTLE - self.MIN_THROTTLE)
                    + self.MIN_THROTTLE
                )
                * 1000
            )
        )

        self.throttle_bl = throttle_bl
        self.pwm_bl.duty_ns(
            int(
                (
                    throttle_bl * (self.MAX_THROTTLE - self.MIN_THROTTLE)
                    + self.MIN_THROTTLE
                )
                * 1000
            )
        )

        self.throttle_br = throttle_br
        self.pwm_br.duty_ns(
            int(
                (
                    throttle_br * (self.MAX_THROTTLE - self.MIN_THROTTLE)
                    + self.MIN_THROTTLE
                )
                * 1000
            )
        )

    def disarm(self):
        print("[LOG] DISARMING")
        self.pwm_fl.deinit()
        self.pwm_fr.deinit()
        self.pwm_bl.deinit()
        self.pwm_br.deinit()
        self.throttle_fl = 0
        self.throttle_fr = 0
        self.throttle_bl = 0
        self.throttle_br = 0
        self.is_armed = False

    def arm(self):
        print("[LOG] ARMING")
        self.pwm_fl.duty_ns(0)
        self.pwm_fr.duty_ns(0)
        self.pwm_bl.duty_ns(0)
        self.pwm_br.duty_ns(0)
        self.pwm_fl.init(freq=self.ESC_FREQUENCY, duty_ns=self.MIN_THROTTLE * 1000)
        self.pwm_fr.init(freq=self.ESC_FREQUENCY, duty_ns=self.MIN_THROTTLE * 1000)
        self.pwm_bl.init(freq=self.ESC_FREQUENCY, duty_ns=self.MIN_THROTTLE * 1000)
        self.pwm_br.init(freq=self.ESC_FREQUENCY, duty_ns=self.MIN_THROTTLE * 1000)
        self.throttle_fl = 0
        self.throttle_fr = 0
        self.throttle_bl = 0
        self.throttle_br = 0
        self.is_armed = True
        utime.sleep(self.ESC_ARM_TIME)
