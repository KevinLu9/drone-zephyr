#!/usr/bin/python3
import time
import serial
import json
import threading
import socket
from data_websocket import WebsocketThread
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput
from camera_stream import CameraThread

ser = serial.Serial(
    port="/dev/serial0",
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=10,
)
msg = ""
i = 0


class UARTSendDataThread(threading.Thread):
    def __init__(self):
        self.quit = False
        threading.Thread.__init__(self)

    def run(self):
        global msg, i
        while not self.quit:
            try:
                i += 1
                payload = {"hello": i}
                print(f"[ZERO] SENDING: {payload}")

                ser.write("{}\n".format(json.dumps(payload)).encode("utf-8"))
                time.sleep(2)
            except:
                pass

    def close(self):
        self.quit = True


class UARTRecvDataThread(threading.Thread):
    def __init__(self, websocket_thread):
        self.websocket_thread = websocket_thread
        self.quit = False
        threading.Thread.__init__(self)

    def run(self):
        recv_data = ""
        while not self.quit:
            try:
                if ser.is_open:
                    b = ser.readline()
                    recv_data += b.decode("utf-8")
                    if recv_data[-1] == "\n":
                        websocket_thread.send_live_data(recv_data)
                        print("[PICO] RECEIVED: ", recv_data)
                    recv_data = ""
                time.sleep(1)
            except:
                pass

    def close(self):
        self.quit = True


# Start Threads
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 0))
host = s.getsockname()[0]  # socket.gethostbyname_ex(socket.gethostname())[2][0]
websocket_port = 8001
cam_port = 8002

websocket_thread = WebsocketThread(host, websocket_port)
uart_send_thread = UARTSendDataThread()
uart_recv_thread = UARTRecvDataThread(websocket_thread)
camera_thread = CameraThread(host, cam_port)

uart_send_thread.start()
uart_recv_thread.start()
websocket_thread.start()
camera_thread.start()


input("PRESS ENTER TO CLOSE")
print("CLOSING Threads")
uart_send_thread.close()
uart_send_thread.close()
websocket_thread.close()
uart_send_thread.join()
uart_recv_thread.join()
websocket_thread.join()
camera_thread.join()
print("[TERMINATION] Program Terminated Successfully")
