import io
import logging
import socketserver
from http import server
import threading

from picamera2 import Picamera2, Preview
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput
import libcamera


class CameraThread(threading.Thread):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.quit = False
        threading.Thread.__init__(self)

    def run(self):
        picam2 = Picamera2()
        preview_config = picam2.create_preview_configuration(
            main={"size": (640, 480)}
        )  # 1920 x 1080 or 640 x 480
        preview_config["transform"] = libcamera.Transform(hflip=1, vflip=1)
        picam2.configure(preview_config)

        global output
        output = StreamingOutput()
        picam2.start_recording(JpegEncoder(), FileOutput(output))
        try:
            address = (self.host, self.port)
            server = StreamingServer(address, StreamingHandler)
            server.serve_forever()
        finally:
            picam2.stop_recording()


class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = threading.Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()


class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(301)
            self.send_header("Location", "/stream.mjpg")
            self.end_headers()
        elif self.path == "/stream.mjpg":
            self.send_response(200)
            self.send_header("Age", 0)
            self.send_header("Cache-Control", "no-cache, private")
            self.send_header("Pragma", "no-cache")
            self.send_header(
                "Content-Type", "multipart/x-mixed-replace; boundary=FRAME"
            )
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b"--FRAME\r\n")
                    self.send_header("Content-Type", "image/jpeg")
                    self.send_header("Content-Length", len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b"\r\n")
            except Exception as e:
                logging.warning(
                    "Removed streaming client %s: %s", self.client_address, str(e)
                )
        else:
            self.send_error(404)
            self.end_headers()


class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True
