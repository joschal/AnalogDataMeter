import time
import RPi.GPIO as GPIO
from fritzconnection.fritzstatus import FritzStatus


status = FritzStatus()
lastRecieved = int(status.bytes_received)
startTime = time.time()


GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
pwm = GPIO.PWM(12, 50)
pwm.start(0)

currentRate = 0
pwm.ChangeDutyCycle(currentRate)


def transition(deltaBytes, deltaTime):
    global currentRate
    endRate = ((deltaBytes + 1) / (6425000 * deltaTime)) * 100

    diff = (endRate - currentRate) / 10
    for i in range(10):
        currentRate = currentRate + diff
        if currentRate >= 100:
            currentRate = 100
        elif currentRate < 1:
            currentRate = 0

        pwm.ChangeDutyCycle(int(currentRate))

        time.sleep(0.5)

while(True):
    status = FritzStatus()

    currentTime = time.time()
    deltaTime = currentTime - startTime

    bytesRecieved = int(status.bytes_received)
    deltaBytes = bytesRecieved - lastRecieved

    transition(deltaBytes, deltaTime)

    lastRecieved = bytesRecieved
    startTime = currentTime
