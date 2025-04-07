from __future__ import print_function

import wiringpi
import json
import time, datetime, sys
import mpu6050

class RFCBot:
    # Class for interacting with the Robot Fight Club RPi0W Bot.
    configfile = "/home/pi/RFCBot/config.json"
    config = {}
    throttle = 1.0
    mpu6050 = {}
    K = 0.98
    K1 = 1 - K
    accel_x_offset = 0
    accel_y_offset = 0
    accel_z_offset = 0
    gyro_x_offset = 0
    gyro_y_offset = 0
    gyro_z_offset = 0
    
    def saveConfig(self):
        data = {}
        data['rfcbot'] = self.config
        with open(self.configfile, 'w') as outfile:
            json.dump(data, outfile, indent=4, sort_keys=True)
        print("Config Saved.", self.config)
        return

    def loadConfig(self):
        with open(self.configfile) as json_file:
            data = json.load(json_file)
        self.config = data['rfcbot']
        print("Config Loaded.")
        #print(self.config)
        return

    def __init__(self):
        # Load the RFCBot config values.
        self.loadConfig()
        
        # Create a new Mpu6050 object
        self.mpu6050 =  mpu6050.mpu6050(0x68)
        if "mpu6050" not in self.config:
            self.calibrateMPU()
        
        # use 'GPIO naming'
        wiringpi.wiringPiSetupGpio()

        # set pins to be a PWM output
        wiringpi.pinMode(self.config['servo']['left']['pin'], wiringpi.GPIO.PWM_OUTPUT)
        wiringpi.pinMode(self.config['servo']['right']['pin'], wiringpi.GPIO.PWM_OUTPUT)

        # set the PWM mode to milliseconds stype
        wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)

        # divide down clock
        wiringpi.pwmSetClock(192)
        wiringpi.pwmSetRange(2000)
        return



    def calibrateMPU(self):
        print ("Reading sensor values for calibration...")
        accel_x_values = []
        accel_y_values = []
        accel_z_values = []
        gyro_x_values = []
        gyro_y_values = []
        gyro_z_values = []
        samples = 1000
        for i in range(samples):
            print("["+str(i)+"/"+str(samples)+"]", end = "\r")
            sys.stdout.flush()
            accel_data = self.mpu6050.get_accel_data()
            accel_x_values.append(accel_data['x'])
            accel_y_values.append(accel_data['y'])
            accel_z_values.append(accel_data['z'])
            
            gyro_data = self.mpu6050.get_gyro_data()
            gyro_x_values.append(gyro_data['x'])
            gyro_y_values.append(gyro_data['y'])
            gyro_z_values.append(gyro_data['z'])
            
            time.sleep(0.005)
        
        accel_x_offset = sum(accel_x_values) / len(accel_x_values)
        accel_y_offset = sum(accel_y_values) / len(accel_y_values)
        accel_z_offset = sum(accel_z_values) / len(accel_z_values)
        gyro_x_offset = sum(gyro_x_values) / len(gyro_x_values)
        gyro_y_offset = sum(gyro_y_values) / len(gyro_y_values)
        gyro_z_offset = sum(gyro_z_values) / len(gyro_z_values)
        
        print ("Calibration complete")
        print("Accel X offset: %s" % accel_x_offset)
        print("Accel Y offset: %s" % accel_y_offset)
        print("Accel Z offset: %s" % accel_z_offset)
        print("Gyro X offset: %s" % gyro_x_offset)
        print("Gyro Y offset: %s" % gyro_y_offset)
        print("Gyro Z offset: %s" % gyro_z_offset)
        
        self.config['mpu6050'] = {}
        self.config['mpu6050']["accel_x_offset"] = accel_x_offset
        self.config['mpu6050']["accel_y_offset"] = accel_y_offset
        self.config['mpu6050']["accel_z_offset"] = accel_z_offset
        self.config['mpu6050']["gyro_x_offset"] = accel_x_offset
        self.config['mpu6050']["gyro_y_offset"] = accel_y_offset
        self.config['mpu6050']["gyro_z_offset"] = accel_z_offset
        self.saveConfig()
        return
        

    def hatToDrive(self, x, y):
        if x == 0 and y == 0:
            self.stop()
        elif x == 0 and y > 0:
            self.forward()        
        elif x == 0 and y < 0:
            self.reverse()
        elif x < 0 and y == 0:
            self.spinleft()
        elif x > 0 and y == 0:
            self.spinright()
        elif x < 0 and y > 0:
            self.turnforwardleft()
        elif x > 0 and y > 0:
            self.turnforwardright()
        elif x < 0 and y < 0:
            self.turnreverseleft()
        elif x > 0 and y < 0:
            self.turnreverseright()
    
    # Define a function to read the sensor data
    def read_mpu6050_data(self):
        # Read the accelerometer values
        accelerometer_data = mpu6050.get_accel_data()

        # Read the gyroscope values
        gyroscope_data = mpu6050.get_gyro_data()

        # Read temp
        temperature = mpu6050.get_temp()

        return accelerometer_data, gyroscope_data, temperature


    def calibrateServo(self, haty):
        L = self.config["servo"]["left"]
        R = self.config["servo"]["right"]
        if joystick.get_button(cbLF):
            L["forward"] += haty
            print("RFC: LF", L["forward"])
        elif joystick.get_button(cbLS):
            L["stop"] += haty
            print("RFC: LS", L["stop"])
        elif joystick.get_button(cbLR):
            L["reverse"] += haty
            print("RFC: LR", L["reverse"])
        elif joystick.get_button(cbRF):
            R["forward"] += haty
            print("RFC: RF", R["forward"])
        elif joystick.get_button(cbRS):
            R["stop"] += haty
            print("RFC: RS", R["stop"])
        elif joystick.get_button(cbRR):
            R["reverse"] += haty
            print("RFC: RR", R["reverse"])

    def setServos(self, leftspeed, rightspeed):
        #print("RFC: Set servos", leftspeed, rightspeed)
        L = self.config['servo']['left']
        R = self.config['servo']['right']
        direction = L["forward"] if leftspeed > 0 else L["reverse"]
        wiringpi.pwmWrite(L["pin"], self.calcPWM(direction, L["stop"], leftspeed))
        direction = R["forward"] if rightspeed > 0 else R["reverse"]
        wiringpi.pwmWrite(R["pin"], self.calcPWM(direction, R["stop"], rightspeed))
        
    def calcPWM(self, direction, stop, throttle):
        return int((direction * throttle) + stop)

    def stop(self):
        #print("RFC: Stop")
        L = self.config['servo']['left']
        R = self.config['servo']['right']
        wiringpi.pwmWrite(L["pin"], L["stop"])
        wiringpi.pwmWrite(R["pin"], R["stop"])

    def forward(self):
        #print("RFC: Forward")
        L = self.config['servo']['left']
        R = self.config['servo']['right']
        wiringpi.pwmWrite(L["pin"], self.calcPWM(L["forward"], L["stop"], self.throttle))
        wiringpi.pwmWrite(R["pin"], self.calcPWM(R["forward"], R["stop"], self.throttle))

    def reverse(self):
        #print("RFC: Reverse", self.throttle)
        L = self.config['servo']['left']
        R = self.config['servo']['right']
        wiringpi.pwmWrite(L["pin"], self.calcPWM(L["reverse"], L["stop"], self.throttle))
        wiringpi.pwmWrite(R["pin"], self.calcPWM(R["reverse"], R["stop"], self.throttle))

    def spinleft(self):
        #print("RFC: Spin left", self.throttle)
        L = self.config['servo']['left']
        R = self.config['servo']['right']
        wiringpi.pwmWrite(L["pin"], self.calcPWM(L["reverse"], L["stop"], self.throttle))
        wiringpi.pwmWrite(R["pin"], self.calcPWM(R["forward"], R["stop"], self.throttle))

    def spinright(self):
        #print("RFC: Spin right", self.throttle)
        L = self.config['servo']['left']
        R = self.config['servo']['right']
        wiringpi.pwmWrite(L["pin"], self.calcPWM(L["forward"], L["stop"], self.throttle))
        wiringpi.pwmWrite(R["pin"], self.calcPWM(R["reverse"], R["stop"], self.throttle))

    def turnforwardleft(self):
        #print("RFC: Turn forward left", self.throttle)
        L = self.config['servo']['left']
        R = self.config['servo']['right']
        wiringpi.pwmWrite(L["pin"], self.calcPWM(L["forward"], L["stop"], self.throttle/2))
        wiringpi.pwmWrite(R["pin"], self.calcPWM(R["forward"], R["stop"], self.throttle))

    def turnforwardright(self):
        #print("RFC: Turn forward right", self.throttle)
        L = self.config['servo']['left']
        R = self.config['servo']['right']
        wiringpi.pwmWrite(L["pin"], self.calcPWM(L["forward"], L["stop"], self.throttle))
        wiringpi.pwmWrite(R["pin"], self.calcPWM(R["forward"], R["stop"], self.throttle/2))

    def turnreverseleft(self):
        #print("RFC: Turn reverse left", self.throttle)
        L = self.config['servo']['left']
        R = self.config['servo']['right']
        wiringpi.pwmWrite(L["pin"], self.calcPWM(L["reverse"], L["stop"], self.throttle/2))
        wiringpi.pwmWrite(R["pin"], self.calcPWM(R["reverse"], R["stop"], self.throttle))

    def turnreverseright(self):
        #print("RFC: Turn reverse right", self.throttle)
        L = self.config['servo']['left']
        R = self.config['servo']['right']
        wiringpi.pwmWrite(L["pin"], self.calcPWM(L["reverse"], L["stop"], self.throttle))
        wiringpi.pwmWrite(R["pin"], self.calcPWM(R["reverse"], R["stop"], self.throttle/2))
