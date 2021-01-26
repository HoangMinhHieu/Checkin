import time
import picamera

camera = picamera.PiCamera()
try:
    camera.start_preview(fullscreen=False, window=(50,151,428,311))
    time.sleep(10)
    camera.stop_preview()
finally:
    camera.close()
    print("da tat roi")