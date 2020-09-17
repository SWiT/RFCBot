import wiringpi
import json

class RFCBot:
    # Class for interacting with the Robot Fight Club RPi0W Bot.
    configfile = "/home/pi/RFCBot/config.json"
    config = {}
    throttle = 1.0
    
    def saveConfig(self):
        data = {}
        data['rfcbot'] = self.config
        with open(self.configfile, 'w') as outfile:
            json.dump(data, outfile, indent=4, sort_keys=True)
        print "Config Saved.", self.config

    def loadConfig(self):
        with open(self.configfile) as json_file:
            data = json.load(json_file)
        self.config = data['rfcbot']
        print "Config Loaded.", self.config


    def __init__(self):
        # Load the RFCBot config values.
        self.loadConfig()
        
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

    def setServos(self, leftspeed, rightspeed):
        #print "RFC: Set servos", leftspeed, rightspeed
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
        #print "RFC: Forward"
        L = self.config['servo']['left']
        R = self.config['servo']['right']
        wiringpi.pwmWrite(L["pin"], self.calcPWM(L["forward"], L["stop"], self.throttle))
        wiringpi.pwmWrite(R["pin"], self.calcPWM(R["forward"], R["stop"], self.throttle))

    def reverse(self):
        #print "RFC: Reverse", self.throttle
        L = self.config['servo']['left']
        R = self.config['servo']['right']
        wiringpi.pwmWrite(L["pin"], self.calcPWM(L["reverse"], L["stop"], self.throttle))
        wiringpi.pwmWrite(R["pin"], self.calcPWM(R["reverse"], R["stop"], self.throttle))

    def spinleft(self):
        #print "RFC: Spin left", self.throttle
        L = self.config['servo']['left']
        R = self.config['servo']['right']
        wiringpi.pwmWrite(L["pin"], self.calcPWM(L["reverse"], L["stop"], self.throttle))
        wiringpi.pwmWrite(R["pin"], self.calcPWM(R["forward"], R["stop"], self.throttle))

    def spinright(self):
        #print "RFC: Spin right", self.throttle
        L = self.config['servo']['left']
        R = self.config['servo']['right']
        wiringpi.pwmWrite(L["pin"], self.calcPWM(L["forward"], L["stop"], self.throttle))
        wiringpi.pwmWrite(R["pin"], self.calcPWM(R["reverse"], R["stop"], self.throttle))

    def turnforwardleft(self):
        #print "RFC: Turn forward left", self.throttle
        L = self.config['servo']['left']
        R = self.config['servo']['right']
        wiringpi.pwmWrite(L["pin"], self.calcPWM(L["forward"], L["stop"], self.throttle/2))
        wiringpi.pwmWrite(R["pin"], self.calcPWM(R["forward"], R["stop"], self.throttle))

    def turnforwardright(self):
        #print "RFC: Turn forward right", self.throttle
        L = self.config['servo']['left']
        R = self.config['servo']['right']
        wiringpi.pwmWrite(L["pin"], self.calcPWM(L["forward"], L["stop"], self.throttle))
        wiringpi.pwmWrite(R["pin"], self.calcPWM(R["forward"], R["stop"], self.throttle/2))

    def turnreverseleft(self):
        #print "RFC: Turn reverse left", self.throttle
        L = self.config['servo']['left']
        R = self.config['servo']['right']
        wiringpi.pwmWrite(L["pin"], self.calcPWM(L["reverse"], L["stop"], self.throttle/2))
        wiringpi.pwmWrite(R["pin"], self.calcPWM(R["reverse"], R["stop"], self.throttle))

    def turnreverseright(self):
        #print "RFC: Turn reverse right", self.throttle
        L = self.config['servo']['left']
        R = self.config['servo']['right']
        wiringpi.pwmWrite(L["pin"], self.calcPWM(L["reverse"], L["stop"], self.throttle))
        wiringpi.pwmWrite(R["pin"], self.calcPWM(R["reverse"], R["stop"], self.throttle/2))
