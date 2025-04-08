from __future__ import print_function

import json, time, datetime, sys
import wiringpi
import mpu6050
import pygame


class RFCBot:
    # Class for interacting with the Robot Fight Club RPi0W Bot.
    configfile = "/home/pi/RFCBot/config.json"
    config = {}
    joystick = {}
    mpu6050 = {}

    throttle = 0.25
    verbose = False
    
    def __init__(self, verbose):
        self.verbose = verbose
        
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
        wiringpi.pwmSetClock(192)   # Rpi has a 19.2MHz PWM clock. Divide it by 192 for 100kHz
        wiringpi.pwmSetRange(2000)  # 2,000/100,000 = 20ms the ideal period for the servo.
        
      
        # Initialize Pygame with no sound.
        pygame.display.init()
        # Initialize any joysticks
        pygame.joystick.init()
        # If no joystick then wait.
        joystickcount = pygame.joystick.get_count() 
        if joystickcount < 1:
            print("RFC: Waiting for Joystick...")
        while joystickcount < 1:
            pygame.joystick.quit()
            time.sleep(1)
            pygame.joystick.init()
            joystickcount = pygame.joystick.get_count()
        # Connect to the first joystick.    
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
        print("RFC: Joystick(0) "+str(self.joystick.get_numbuttons())+" Buttons")
        
        return
        
        
    def saveConfig(self):
        data = {}
        data['rfcbot'] = self.config
        with open(self.configfile, 'w') as outfile:
            json.dump(data, outfile, indent=4, sort_keys=True)
        if self.verbose: print("RFC: Config Saved.", self.config)
        return


    def loadConfig(self):
        with open(self.configfile) as json_file:
            data = json.load(json_file)
        self.config = data['rfcbot']
        print("RFC: Config Loaded.")
        if self.verbose:
            pretty_json = json.dumps(self.config, indent=4)
            print(pretty_json)
        
        return


    def calibrateMPU(self):
        print ("RFC: Reading sensor values for calibration...")
        accel_x_values = []
        accel_y_values = []
        accel_z_values = []
        gyro_x_values = []
        gyro_y_values = []
        gyro_z_values = []
        samples = 1000
        for i in range(samples):
            print("RFC: ["+str(i)+"/"+str(samples)+"]", end = "\r")
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
        
        print ("RFC: Calibration complete")
        print("RFC: accel_x_offset %s" % accel_x_offset)
        print("RFC: accel_y_offset %s" % accel_y_offset)
        print("RFC: accel_z_offset %s" % accel_z_offset)
        print("RFC: gyro_x_offset %s" % gyro_x_offset)
        print("RFC: gyro_y_offset %s" % gyro_y_offset)
        print("RFC: gyro_z_offset %s" % gyro_z_offset)
        
        self.config['mpu6050'] = {}
        self.config['mpu6050']["accel_x_offset"] = accel_x_offset
        self.config['mpu6050']["accel_y_offset"] = accel_y_offset
        self.config['mpu6050']["accel_z_offset"] = accel_z_offset
        self.config['mpu6050']["gyro_x_offset"] = gyro_x_offset
        self.config['mpu6050']["gyro_y_offset"] = gyro_y_offset
        self.config['mpu6050']["gyro_z_offset"] = gyro_z_offset
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
    
    # Read the accelerometer data and apply any offset
    def get_accel_data(self):
        cfg = self.config["mpu6050"]
        accel_data = self.mpu6050.get_accel_data()
        accel_data['x'] -= cfg["accel_x_offset"]
        accel_data['y'] -= cfg["accel_y_offset"]
        accel_data['z'] -= cfg["accel_z_offset"]
        return accel_data

    # Read the accelerometer data and apply any offset
    def get_gyro_data(self):
        cfg = self.config["mpu6050"]
        gyro_data = self.mpu6050.get_gyro_data()
        gyro_data['x'] -= cfg["gyro_x_offset"]
        gyro_data['y'] -= cfg["gyro_y_offset"]
        gyro_data['z'] -= cfg["gyro_z_offset"]
        return gyro_data


    def calibrateServo(self, haty):
        cfg = self.config
        L = cfg["servo"]["left"]
        R = cfg["servo"]["right"]
        
        if self.joystick.get_button(cfg["btnCalLF"]):
            L["forward"] += haty
            print("RFC: LF", L["forward"])
        elif self.joystick.get_button(cfg["btnCalLS"]):
            L["stop"] += haty
            print("RFC: LS", L["stop"])
        elif self.joystick.get_button(cfg["btnCalLR"]):
            L["reverse"] += haty
            print("RFC: LR", L["reverse"])
        elif self.joystick.get_button(cfg["btnCalRF"]):
            R["forward"] += haty
            print("RFC: RF", R["forward"])
        elif self.joystick.get_button(cfg["btnCalRS"]):
            R["stop"] += haty
            print("RFC: RS", R["stop"])
        elif self.joystick.get_button(cfg["btnCalRR"]):
            R["reverse"] += haty
            print("RFC: RR", R["reverse"])

    def setServos(self, leftspeed, rightspeed):
        if self.verbose: print("RFC: Set servos", leftspeed, rightspeed)
        L = self.config['servo']['left']
        R = self.config['servo']['right']
        
        direction = L["forward"] if leftspeed > 0 else L["reverse"]
        wiringpi.pwmWrite(L["pin"], self.calcPWM(direction, L["stop"], abs(leftspeed)))
        
        direction = R["forward"] if rightspeed < 0 else R["reverse"]
        wiringpi.pwmWrite(R["pin"], self.calcPWM(direction, R["stop"], abs(rightspeed)))
        
    def calcPWM(self, direction, stop, throttle):
        return int(stop - ((stop - direction) * throttle))
        
    
    def stop(self):
        if self.verbose: print("RFC: Stop")
        L = self.config['servo']['left']
        R = self.config['servo']['right']
        wiringpi.pwmWrite(L["pin"], L["stop"])
        wiringpi.pwmWrite(R["pin"], R["stop"])

    def forward(self):
        if self.verbose: print("RFC: Forward")
        L = self.config['servo']['left']
        R = self.config['servo']['right']
        wiringpi.pwmWrite(L["pin"], L["forward"])
        wiringpi.pwmWrite(R["pin"], R["forward"])

    def reverse(self):
        if self.verbose: print("RFC: Reverse")
        L = self.config['servo']['left']
        R = self.config['servo']['right']
        wiringpi.pwmWrite(L["pin"], L["reverse"])
        wiringpi.pwmWrite(R["pin"], R["reverse"])

    def spinleft(self):
        if self.verbose: print("RFC: Spin left")
        L = self.config['servo']['left']
        R = self.config['servo']['right']
        wiringpi.pwmWrite(L["pin"], L["reverse"])
        wiringpi.pwmWrite(R["pin"], R["forward"])

    def spinright(self):
        if self.verbose: print("RFC: Spin right")
        L = self.config['servo']['left']
        R = self.config['servo']['right']
        wiringpi.pwmWrite(L["pin"], L["forward"])
        wiringpi.pwmWrite(R["pin"], R["reverse"])

    def turnforwardleft(self):
        if self.verbose: print("RFC: Turn forward left", self.throttle)
        L = self.config['servo']['left']
        R = self.config['servo']['right']
        wiringpi.pwmWrite(L["pin"], self.calcPWM(L["forward"], L["stop"], self.throttle))
        wiringpi.pwmWrite(R["pin"], R["forward"])

    def turnforwardright(self):
        if self.verbose: print("RFC: Turn forward right", self.throttle)
        L = self.config['servo']['left']
        R = self.config['servo']['right']
        wiringpi.pwmWrite(L["pin"], L["forward"])
        wiringpi.pwmWrite(R["pin"], self.calcPWM(R["forward"], R["stop"], self.throttle))

    def turnreverseleft(self):
        if self.verbose: print("RFC: Turn reverse left", self.throttle)
        L = self.config['servo']['left']
        R = self.config['servo']['right']
        wiringpi.pwmWrite(L["pin"], self.calcPWM(L["reverse"], L["stop"], self.throttle))
        wiringpi.pwmWrite(R["pin"], R["reverse"])

    def turnreverseright(self):
        if self.verbose: print("RFC: Turn reverse right", self.throttle)
        L = self.config['servo']['left']
        R = self.config['servo']['right']
        wiringpi.pwmWrite(L["pin"], L["reverse"])
        wiringpi.pwmWrite(R["pin"], self.calcPWM(R["reverse"], R["stop"], self.throttle))
