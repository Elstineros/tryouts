from flask import Flask,render_template,url_for,request,redirect, make_response
import random
import json
from time import time
from random import random
from flask import Flask, render_template, make_response, jsonify
from mpu6050 import mpu6050
import csv

app = Flask(__name__)

mpu = mpu6050(0x68)


@app.route('/', methods=["GET", "POST"])
def main():
    return render_template('index.html')

@app.route('/data', methods=["GET"])
def data():
    # Data Format
    # [TIME, Temperature, Humidity]
    accel_data = mpu.get_accel_data()
    Temperature = accel_data['x']
    Humidity = 55

    data = [time() * 1000, Temperature, Humidity]

    response = make_response(json.dumps(data))

    response.content_type = 'application/json'

    return response

@app.route('/input', methods=["GET", "POST"])
def input():
    sliderInput = request.args.get('sliderInput')
    print("sliderInput : "+sliderInput)
    return sliderInput


if __name__ == "__main__":
    app.run(debug=True)
