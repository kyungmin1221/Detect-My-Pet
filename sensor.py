#sensor.py

import RPi.GPIO as GPIO
import os; import io; import time
import picamera
import cv2; import numpy as np
import Adafruit_MCP3008
import busio
from adafruit_htu21d import HTU21D

trig = 20
echo =16

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(trig,GPIO.OUT)
GPIO.setup(echo,GPIO.IN)
GPIO.output(trig,False)

sda=2
scl=3

i2c=busio.I2C(scl,sda)
sensor=HTU21D(i2c)
mcp = Adafruit_MCP3008.MCP3008(clk=11,cs=8,miso=9,mosi=10)

fileName = ""
stream = io.BytesIO()
camera = picamera.PiCamera()
camera.start_preview()
camera.rotation = 180
camera.resolution = (640,480 )
camera.framerate = 15
camera.resolution = (320, 240)
time.sleep(1)
mcp=Adafruit_MCP3008.MCP3008(clk=11,cs=8,miso=9,mosi=10)

led_red = 6
led_yello =19
buzzer = 18
GPIO.setup(led_red,GPIO.OUT)
GPIO.setup(led_yello,GPIO.OUT)
GPIO.setup(buzzer,GPIO.OUT)
pwm = GPIO.PWM(buzzer,262)



def getLight():
        if mcp.read_adc(0)>200:
                return "밝음"
        else:
                return "밝지않음"

def Speaker():
        pwm.start(50.0)
        time.sleep(1.5)
        pwm.stop()

def SpeakerOff():
        pwm.stop()

def measureDistance():
        global trig,echo
        time.sleep(0.5)
        GPIO.output(trig,True)
        time.sleep(0.0001)
        GPIO.output(trig,False)

        while(GPIO.input(echo)==0):
        #       pass
                pulse_start = time.time()
        while(GPIO.input(echo)==1):
        #       pass
                pulse_end=time.time()

        pulse_duration = pulse_end - pulse_start
        return 340*100/2*pulse_duration


def ledIn():
        onOff = 1
        controlLED(led_red , onOff)
        controlLED(led_yello,onOff)

def controlLED(Led,onOff):
        GPIO.output(led_red,onOff)
        GPIO.output(led_yello,onOff)


def ledOut():
        onOff = 0
        controlLED(led_red,onOff)
        controlLED(led_yello,onOff)


def takePicture() :
        global fileName, stream, camera

        if len(fileName) != 0:
                os.unlink(fileName)

        stream.seek(0)
        stream.truncate()
        camera.capture(stream, format='jpeg', use_video_port=True)
        data = np.frombuffer(stream.getvalue(), dtype=np.uint8)
        image = cv2.imdecode(data, 1)
        haar = cv2.CascadeClassifier('./haarCascades/haar-cascade-files-master/haarcascade_frontalface_default.xml')
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = haar.detectMultiScale(image_gray,1.1,3)
        for x, y, w, h in faces:
                cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

        takeTime = time.time()
        fileName = "./static/%d.jpg" % (takeTime * 10)
        cv2.imwrite(fileName, image)
        return fileName

if __name__ == '__main__' :
        while(True):
                name = takePicture()
                distance = measureDistance()
                if mcp.read_adc (0 )>200:
                        print("밝음")
                elif mcp.read_adc (0 )>130 and mcp.read_adc(0 )<180 :
                        print("밝지않음")
                else:
                        print("어두움")
                        print("distance=%f" % distance)
