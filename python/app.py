from flask import Flask,render_template,url_for,request,redirect, make_response
import random
import json
from time import time
from random import random
from flask import Flask, render_template, make_response
from mpu6050 import mpu6050
import csv

app = Flask(__name__)

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
    return steeringInput

@app.route('/throttle', methods=["GET", "POST"])
def throttle():
    throttleInput = request.args.get('throttleInput')
    print("throttleInput : "+throttleInput)
    return throttleInput

if __name__ == "__main__":
    app.run(debug=True)
