from machine import UART, Pin, ADC
import time
import json
import asyncio


class UARTToPiZero:
    def __init__(
        self,
        uart,
        orientation_lock,
        drone_orientation,
        motor_lock,
        motors,
        adc_voltage_pin,
    ):
        self.uart = uart
        self.orientation_lock = orientation_lock
        self.drone_orientation = drone_orientation
        self.motor_lock = motor_lock
        self.motors = motors
        self.voltage_adc = ADC(Pin(adc_voltage_pin))
        self.battery_voltage = 0
        self.SEND_DATA_FREQUENCY = 0.5  # In HERTS
        self.RECV_DATA_FREQUENCY = 10  # In HERTS

    def run(self):
        uart_send_task = asyncio.create_task(self.uart_send())
        uart_recv_task = asyncio.create_task(self.uart_recv())
        await uart_send_task
        await uart_recv_task
        # asyncio.run(self.uart_connection())

    async def uart_send(self):
        while True:
            try:
                self.battery_voltage = (
                    self.voltage_adc.read_u16() / 65535 * 18.3
                )  # read value, 0-65535 across voltage range 0.0v - 3.3v
                # Grab Live data from drone sensors
                self.orientation_lock.acquire()
                self.motor_lock.acquire()
                live_data = {
                    "pitch": self.drone_orientation.pitch,
                    "roll": self.drone_orientation.roll,
                    "yaw": self.drone_orientation.yaw,
                    "tilt_x": self.drone_orientation.tilt_x,
                    "tilt_y": self.drone_orientation.tilt_y,
                    "tilt_z": self.drone_orientation.tilt_z,
                    "is_armed": self.motors.is_armed,
                    "battery_voltage": self.battery_voltage,
                }
                self.motor_lock.release()
                self.orientation_lock.release()

                self.uart.write("{}\n".format(json.dumps(live_data)).encode("utf-8"))
                await asyncio.sleep(1 / self.SEND_DATA_FREQUENCY)
            except Exception as e:
                print(e)

    async def uart_recv(self):
        msg = ""
        while True:
            try:
                if self.uart.any():
                    b = self.uart.readline()

                    msg += b.decode("utf-8")
                    if msg[-1] == "\n":
                        print("[UART] RECEIVED: " + msg)
                        # recv_data = json.loads(msg)
                        msg = ""
                # await asyncio.sleep(1 / self.RECV_DATA_FREQUENCY)
            except Exception as e:
                print(e)
