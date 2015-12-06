import time
import RPi.GPIO as GPIO
from fritzconnection.fritzstatus import FritzStatus


status = FritzStatus()
lastRecieved = int(status.bytes_received)
startTime = time.time()

GPIO.cleanup()

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
pwm = GPIO.PWM(12, 500)
pwm.start(50)

while(True):
    status = FritzStatus()

    currentTime = time.time()
    deltaTime = currentTime - startTime

    bytesRecieved = int(status.bytes_received)
    deltaBytes = (bytesRecieved - lastRecieved) / deltaTime

    lastRecieved = bytesRecieved
    startTime = currentTime

    rate = ((deltaBytes + 1) / (6425000 * deltaTime)) * 100

    if rate > 90:
        rate = 90
    elif rate < 4:
        rate = 0

    pwm.ChangeDutyCycle(int(rate))

    time.sleep(1)
