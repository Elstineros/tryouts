import smbus			#import SMBus module of I2C
from time import sleep          #import
import csv
import time
import datetime



#some MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47
TEMP_OUT_H   = 0x41
Gxx = 0
Gyy = 0
Gzz = 0


from flask import render_template, url_for, request
from flask import Flask
app = Flask(__name__)  
@app.route('/')
	
	
	
def index():
		
	return render_template("sensor.html",GyroX=Gxx, GyroY=Gyy, GyroZ=Gzz )

	
	
	

if __name__ == "__main__":
	app.run(debug=True)  




def MPU_Init():
	#write to sample rate register
	bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
	
	#Write to power management register
	bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
	
	#Write to Configuration register
	bus.write_byte_data(Device_Address, CONFIG, 0)
	
	#Write to Gyro configuration register
	bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
	
	#Write to interrupt enable register
	bus.write_byte_data(Device_Address, INT_ENABLE, 1)
	
	bus.write_byte_data(Device_Address1, SMPLRT_DIV, 7)
	
	#Write to power management register
	bus.write_byte_data(Device_Address1, PWR_MGMT_1, 1)
	
	#Write to Configuration register
	bus.write_byte_data(Device_Address1, CONFIG, 0)
	
	#Write to Gyro configuration register
	bus.write_byte_data(Device_Address1, GYRO_CONFIG, 24)
	
	#Write to interrupt enable register
	bus.write_byte_data(Device_Address1, INT_ENABLE, 1)

def read_raw_data(addr):
	#Accelero and Gyro value are 16-bit
        high = bus.read_byte_data(Device_Address, addr)
        low = bus.read_byte_data(Device_Address, addr+1)
       
    
        #concatenate higher and lower value
        value = ((high << 8) | low)
        
        #to get signed value from mpu6050
        if(value > 32768):
                value = value - 65536
        return value
    

def read_raw_data1(addr):
	#Accelero and Gyro value are 16-bit
        
        high1 = bus.read_byte_data(Device_Address1, addr)
        low1 = bus.read_byte_data(Device_Address1, addr+1)
    
        #concatenate higher and lower value
        value1 = ((high1 << 8) | low1)
              
        #to get signed value from mpu6050
        if(value1 > 32768):
                value1 = value1 - 65536
        return value1




    
bus = smbus.SMBus(1) 	# or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x68   # MPU6050 device address
Device_Address1 = 0x69

MPU_Init()

print (" Reading Data of Gyroscope and Accelerometer")

while True:
	
	#Read Accelerometer raw value
	acc_x = read_raw_data(ACCEL_XOUT_H)
	acc_y = read_raw_data(ACCEL_YOUT_H)
	acc_z = read_raw_data(ACCEL_ZOUT_H)
	
	#Read Gyroscope raw value
	gyro_x = read_raw_data(GYRO_XOUT_H)
	gyro_y = read_raw_data(GYRO_YOUT_H)
	gyro_z = read_raw_data(GYRO_ZOUT_H)
	
	#Full scale range +/- 250 degree/C as per sensitivity scale factor
	Ax = acc_x/16384.0
	Ay = acc_y/16384.0
	Az = acc_z/16384.0
	
	Gx = gyro_x/131.0
	Gy = gyro_y/131.0
	Gz = gyro_z/131.0
	
	#f = open('gyrodata.csv','w') # open the file in write mode
	#f.write(str(Gx)+ ','+str(Gy)+','+str(Gz)+'\n') # write the data to the file with commas between the data and a 'return' at the end
	#f.close() # close the file
	acc_x1 = read_raw_data1(ACCEL_XOUT_H)
	acc_y1 = read_raw_data1(ACCEL_YOUT_H)
	acc_z1 = read_raw_data1(ACCEL_ZOUT_H)
	
	#Read Gyroscope raw value
	gyro_x1 = read_raw_data1(GYRO_XOUT_H)
	gyro_y1 = read_raw_data1(GYRO_YOUT_H)
	gyro_z1 = read_raw_data1(GYRO_ZOUT_H)
	
	#Full scale range +/- 250 degree/C as per sensitivity scale factor
	Ax1 = acc_x1/16384.0
	Ay1 = acc_y1/16384.0
	Az1 = acc_z1/16384.0
	
	Gx1 = gyro_x1/131.0
	Gy1 = gyro_y1/131.0
	Gz1 = gyro_z1/131.0
	
	global Gxx
	global Gyy
	global Gzz
	
	Gxx = (Gx + Gx1 )/2
	Gyy = (Gy + Gy1 )/2
	Gzz = (Gz + Gz1 )/2
	
	Axx = (Ax + Ax1 )/2
	Ayy = (Ay + Ay1 )/2
	Azz = (Az + Az1 )/2
	
	# the a is for append, if w for write is used then it overwrites the file
	with open('gyrodata.csv', mode='a') as sensor_readings:
	    today = datetime.datetime.now().strftime("%Y-%m-%d")
	    now = datetime.datetime.now().strftime("%H:%M:%S")
	    sensor_write = csv.writer(sensor_readings, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	    write_to_log = sensor_write.writerow([str(today),str(now),Gxx,Gyy,Gzz,Axx,Ayy,Azz])
	 
	print ("Gx=%.2f" %Gxx, "Gy=%.2f" %Gyy,  "Gz=%.2f" %Gzz, "Ax=%.2f g" %Axx, "Ay=%.2f g" %Ayy, "Az=%.2f g" %Azz)

	sleep(1)

