from flask import Flask,render_template,url_for,request,redirect, make_response
import random
import json
from time import time
from random import random
from flask import Flask, render_template, make_response
from mpu6050 import mpu6050
import csv
from RaspberryMotors.motors import servos
import RPi.GPIO as GPIO
import pigpio

GPIO.setwarnings(False)
servos.setMode(GPIO.BCM)
# GPIO.setup(12,GPIO.OUT)
# p=GPIO.PWM(12,100)
# p.start(0)
app = Flask(__name__)
pig = pigpio.pi()

mpu = mpu6050(0x68)

@app.route('/', methods=["GET", "POST"])
def main():
    return render_template('index.html')


@app.route('/data', methods=["GET", "POST"])
def data():
    # Data Format
    # [TIME, Temperature, Humidity]
    accel_data = mpu.get_accel_data()
    gyro_data = mpu.get_gyro_data()
    
    AccX = accel_data['x'] / 16384.0
    AccY = accel_data['y'] / 16384.0
    AccZ = accel_data['z'] / 16384.0
    GyroX = gyro_data['x'] / 131.0
    GyroY = gyro_data['y'] / 131.0
    GyroZ = gyro_data['z'] / 131.0
    

    data = [time() * 1000, AccX, AccY, AccZ, GyroX, GyroY, GyroZ]

    response = make_response(json.dumps(data))

    response.content_type = 'application/json'

    return response

@app.route('/steering', methods=["GET", "POST"])
def steering():
    steeringInput = request.args.get('steeringInput')

    print("steeringInput : "+steeringInput)
    servos.ResetGpioAtShutdown(False)
    #pig.set_servo_pulsewidth(12, steeringInput)
    servos.setMode(GPIO.BCM) # refer to the pins by the "Broadcom SOC channel" number
    servos.ResetGpioAtShutdown(False) # do not reset GPIO at last servo shutdown
    s1 = servos.servo(23)
    s1.setAngleAndWait(steeringInput, 0.5) # move to position of 180 degrees
    s1.shutdown();
    #GPIO.cleanup()
   
    return steeringInput

@app.route('/throttle', methods=["GET", "POST"])
def throttle():
    throttleInput = request.args.get('throttleInput')
    print("throttleInput : "+throttleInput)
    pig.set_servo_pulsewidth(12, throttleInput)
    
    return throttleInput

if __name__ == "__main__":
    app.run(debug=True)
