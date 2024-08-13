import asyncio
import socket
import websockets
import json
import threading
import time

CLIENTS = set()
LIVE_DATA_RATE_SEC = 1


class WebsocketThread(threading.Thread):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.quit = False
        threading.Thread.__init__(self)

    def run(self):
        async def run_tasks():
            print(f"[LOG] Starting WebSocket Server on {self.host}:{self.port}")
            async with websockets.serve(self.handle_connection, self.host, self.port):
                await asyncio.Future()  # run forever

        asyncio.run(run_tasks())

    def close(self):
        self.quit = True

    async def handle_recv(self, websocket):
        try:
            while not self.quit:
                message = await websocket.recv()
                print(message)
        except:
            pass

    def send(self, websocket, data):
        try:
            websocket.send(data)
        except:
            pass

    def send_live_data(self, live_data):
        try:
            websockets.broadcast(CLIENTS, live_data)
        except:
            pass

    def test_send_live_data(self):
        while True:
            self.send_live_data(
                json.dumps({"is_armed": False, "pitch": 0, "roll": 0, "yaw": 0})
            )
            time.sleep(LIVE_DATA_RATE_SEC)

    async def handle_connection(self, websocket):
        CLIENTS.add(websocket)
        host_addr = websocket.remote_address[0]
        print(f"[LOG] New Connection with: {host_addr}")
        try:
            recv_task = asyncio.create_task(self.handle_recv(websocket))
            # If either tasks fail, cancel the other task and close connection.
            done, pending = await asyncio.wait(
                [recv_task], return_when=asyncio.FIRST_COMPLETED
            )
            for task in pending:
                task.cancel()
        except Exception as e:
            print(f"[ERROR] Error Occurred with: {host_addr} > {e}")
        finally:
            CLIENTS.remove(websocket)
            print(f"[LOG] Connection Lost with: {host_addr}")


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 0))
    host = s.getsockname()[0]  # socket.gethostbyname_ex(socket.gethostname())[2][0]
    port = 8001

    websocket_thread = WebsocketThread(host, port)
    websocket_thread.start()
    websocket_thread.test_send_live_data()
