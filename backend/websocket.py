import asyncio
import socket
import websockets
import json

CLIENTS = set()
LIVE_DATA_RATE_SEC = 1


async def handle_recv(websocket):
    try:
        while True:
            message = await websocket.recv()
            print(message)
    except:
        pass


async def handle_send(websocket):
    try:
        while True:
            # await websocket.send("Test outgoing")
            await asyncio.sleep(LIVE_DATA_RATE_SEC)
    except:
        pass


async def send_live_data():
    try:
        while True:
            live_data = {"armed": True}
            websockets.broadcast(CLIENTS, json.dumps(live_data))
            await asyncio.sleep(LIVE_DATA_RATE_SEC)
    except:
        pass


async def handle_connection(websocket):
    CLIENTS.add(websocket)
    host_addr = websocket.remote_address[0]
    print(f"[LOG] New Connection with: {host_addr}")
    try:
        recv_task = asyncio.create_task(handle_recv(websocket))
        send_task = asyncio.create_task(handle_send(websocket))
        # If either tasks fail, cancel the other task and close connection.
        done, pending = await asyncio.wait(
            [recv_task, send_task], return_when=asyncio.FIRST_COMPLETED
        )
        for task in pending:
            task.cancel()
        # while True:
        #   message = await websocket.recv()
        #   print(message)
        #   msg = {"armed": True}
        #   await websocket.send(json.dumps(msg))
        #   websockets.broadcast(CLIENTS, msg)
    except Exception as e:
        print(f"[ERROR] Error Occurred with: {host_addr} > {e}")
    finally:
        CLIENTS.remove(websocket)
        print(f"[LOG] Connection Lost with: {host_addr}")


host = socket.gethostbyname_ex(socket.gethostname())[2][0]
port = 8001


async def main():
    print(f"[LOG] Starting WebSocket Server on {host}:{port}")
    asyncio.create_task(send_live_data())
    async with websockets.serve(handle_connection, host, port):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
