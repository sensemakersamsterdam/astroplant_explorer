import time
import picamera

with picamera.PiCamera() as camera:
    camera.start_preview()
    time.sleep(10)
    camera.stop_preview()