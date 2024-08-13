import machine
import asyncio
import _thread
import time
import sys
from drone_orientation import DroneOrientation
from motors import Motors
from uart import UARTToPiZero

# First thread, gets data from IMU to predict drone orientation.
def thread_1():
    global drone_orientation, orientation_lock
    global motors, motor_pin_fl, motor_pin_fr, motor_pin_bl, motor_pin_br
    global pi_zero_connection
    global quit_flag
    
    async def run_thread_1():
        drone_orientation_task = asyncio.create_task(drone_orientation.run())
        uart_send_task = asyncio.create_task(pi_zero_connection.uart_send())
        uart_recv_task = asyncio.create_task(pi_zero_connection.uart_recv())
        await drone_orientation_task
        await uart_send_task
        await uart_recv_task
        
    asyncio.run(run_thread_1())


# Second thread, handles motor speeds.
def thread_2():
    global drone_orientation, orientation_lock
    global motors, motor_pin_fl, motor_pin_fr, motor_pin_bl, motor_pin_br
    global quit_flag
    motors.run(motor_pin_fl, motor_pin_fr, motor_pin_bl, motor_pin_br)

# main
try:
    # Shared Memory
    i2c = machine.I2C(0, sda=machine.Pin(4), scl=machine.Pin(5), freq=400000)
    motor_pin_fl = 20
    motor_pin_fr = 18
    motor_pin_bl = 21
    motor_pin_br = 19
    adc_voltage_pin = 28
    uart = machine.UART(1, baudrate=115200, tx=machine.Pin(8), rx=machine.Pin(9))
    
    # Locks
    orientation_lock = _thread.allocate_lock()
    motor_lock = _thread.allocate_lock()
    # Class Instances
    drone_orientation = DroneOrientation(i2c, orientation_lock, motor_lock)
    motors = Motors(orientation_lock, drone_orientation, motor_lock)
    pi_zero_connection = UARTToPiZero(uart, orientation_lock, drone_orientation, motor_lock, motors, adc_voltage_pin)
    quit_flag = False
    

    # Start threads
    thread_1 = _thread.start_new_thread(thread_1, ())
    thread_2()
except Exception as e:
    print("[ERROR]: The following traceback was found:")
    print("-----------------------------------------------")
    sys.print_exception(e)
    print("-----------------------------------------------")
except KeyboardInterrupt as e:
    print("[KEYBOARD INTERRUPT]: In Main - Manually Stopping")
    print("-----------------------------------------------")
    sys.print_exception(e)
    print("-----------------------------------------------")
finally:
    # Correctly close threads, coroutines and reset device
    drone_orientation.close()
    motors.close()
    machine.reset()

    
