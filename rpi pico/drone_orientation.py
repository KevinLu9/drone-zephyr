import utime
import asyncio
import math
import sys
from mpu6050 import init_mpu6050, get_mpu6050_data

class DroneOrientation():
    # Constructor
    def __init__(self, i2c, orientation_lock, motor_lock):
        self.pitch = 0
        self.roll = 0
        self.yaw = 0
        self.tilt_x = 0
        self.tilt_y = 0
        self.tilt_z = 0
        self.alpha = 0.98 # Alpha constant for Complimentary Filter.
        self.poll_frequency = 250 # Target Poll Frequency to calculate orientation from MPU6050 in Hz.
        self.i2c = i2c # The i2c object to use to interface with MPU6050.
        self.quit = False
        self.orientation_lock = orientation_lock
        self.motor_lock = motor_lock
    
    # Calculates the tilt angle of the drone based on accelerometer data.
    def _calculate_tilt_angles(self, accel_data):
        x, y, z = accel_data['x'], accel_data['y'], accel_data['z']
     
        tilt_x = math.atan2(y, math.sqrt(x * x + z * z)) * 180 / math.pi
        tilt_y = math.atan2(-x, math.sqrt(y * y + z * z)) * 180 / math.pi
        tilt_z = math.atan2(z, math.sqrt(x * x + y * y)) * 180 / math.pi
         
        self.tilt_x = tilt_x
        self.tilt_y = tilt_y
        self.tilt_z = tilt_z
         
        return tilt_x, tilt_y, tilt_z
     
    # Calculates the Pitch and Roll of the drone based on accelerometer and Gyroscope Data from the MPU6050.
    def _complementary_filter(self, gyro_data, accel_data, dt, alpha=0.98): # alpha = 0.98
        # Calculate Tilt angles
        x, y, z = accel_data['x'], accel_data['y'], accel_data['z']
        tilt_x, tilt_y, tilt_z = self._calculate_tilt_angles(accel_data)
        
        # Calculate gyroscope delta angles
        gyro_x = gyro_data['x'] * dt
        gyro_y = gyro_data['y'] * dt
        gyro_z = gyro_data['z'] * dt
        
        # Weighted Average on accelerometer tilt angle and Gyroscope delta angles
        pitch = alpha * (self.pitch + gyro_x) + (1 - alpha) * tilt_x
        roll = alpha * (self.roll + gyro_y) + (1 - alpha) * tilt_y
        yaw = 0 # Yaw cannot be calculated due to abscence of magnetometer
        
        return pitch, roll, yaw

    async def run(self):
        init_mpu6050(self.i2c)
        prev_time = utime.ticks_ms()
        try:
            while not self.quit:
                data = get_mpu6050_data(self.i2c)
                curr_time = utime.ticks_ms()
                dt = (curr_time - prev_time) / 1000

                self.orientation_lock.acquire()
                self.pitch, self.roll, self.yaw = self._complementary_filter(data['gyro'], data['accel'], dt)
                self.orientation_lock.release()
             
                #print("Temperature: {:.2f} °C".format(data['temp']))
                #print("Tilt angles: X: {:.2f}, Y: {:.2f}, Z: {:.2f} degrees".format(tilt_x, tilt_y, tilt_z))
                #print("Pitch: {:.2f}, Roll: {:.2f} Yaw: {:.2f} degrees, dt: {:.2f} ms".format(self.pitch, self.roll, self.yaw, dt*1000), end="\r")
                
                # Wait for correct time to make Hz the target poll frequency
                prev_time = curr_time
                elapsed_time = utime.ticks_ms() - curr_time
                if (elapsed_time / 1000) < (1 / self.poll_frequency): 
                    await asyncio.sleep((1 / self.poll_frequency) - (elapsed_time / 1000))
        except Exception as e:
            print("[ERROR]: The following traceback was found:")
            print("-----------------------------------------------")
            sys.print_exception(e)
            print("-----------------------------------------------")
        except KeyboardInterrupt as e:
            print("[KEYBOARD INTERRUPT]: In Drone Orientation - Manually Stopping")
            print("-----------------------------------------------")
            sys.print_exception(e)
            print("-----------------------------------------------")
        quit_flag = True
        print("[TERMINATION] Drone Orientation Coroutine")
    
    def close(self):
        self.quit = True