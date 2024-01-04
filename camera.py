from picamera2 import Picamera2
picam2 = Picamera2()
picam2.start_and_capture_file("image.jpg", delay=1, show_preview=False)