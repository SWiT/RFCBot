import wiringpi

class RFCBot:
    # Class for interacting with the Robot Fight Club RPi0W Bot.
    
    servoleft = 18      # Left servo GPIO pin
    servoright = 13     # Right servo GPIO pin

    LF = 50     # Max offset for the left servos forward direction
    LS = 147    # The left servos stopped position
    LR = -50    # Max offset for the left servos reverse direction

    RF = -50
    RS = 147
    RR = 50

    throttle = 1.0
    accel = 0.05
    
    def __init__(self):
        # use 'GPIO naming'
        wiringpi.wiringPiSetupGpio()

        # set #18 to be a PWM output
        wiringpi.pinMode(self.servoleft, wiringpi.GPIO.PWM_OUTPUT)
        wiringpi.pinMode(self.servoright, wiringpi.GPIO.PWM_OUTPUT)

        # set the PWM mode to milliseconds stype
        wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)

        # divide down clock
        wiringpi.pwmSetClock(192)
        wiringpi.pwmSetRange(2000)

    def setServos(self, leftspeed, rightspeed):
        print "RFC: Set servos", leftspeed, rightspeed
        wiringpi.pwmWrite(self.servoleft, self.calcPWM(self.LF, self.LS, leftspeed))
        wiringpi.pwmWrite(self.servoright, self.calcPWM(self.RF, self.RS, rightspeed))
        
    def calcPWM(self, direction, stop, throttle):
        return int((direction * throttle) + stop)
    
    def stop(self):
        print("RFC: Stop")
        wiringpi.pwmWrite(self.servoleft, self.LS)
        wiringpi.pwmWrite(self.servoright, self.RS)
        
    def forward(self):
        print "RFC: Forward"
        wiringpi.pwmWrite(self.servoleft, self.calcPWM(self.LF, self.LS, self.throttle))
        wiringpi.pwmWrite(self.servoright, self.calcPWM(self.RF, self.RS, self.throttle))
        
    def reverse(self):
        print "RFC: Reverse", self.throttle 
        wiringpi.pwmWrite(self.servoleft, self.calcPWM(self.LR, self.LS, self.throttle))
        wiringpi.pwmWrite(self.servoright, self.calcPWM(self.RR, self.RS, self.throttle))
    
    def spinleft(self):
        print "RFC: Spin left", self.throttle
        wiringpi.pwmWrite(self.servoleft, self.calcPWM(self.LR, self.LS, self.throttle))
        wiringpi.pwmWrite(self.servoright, self.calcPWM(self.RF, self.RS, self.throttle))
            
    def spinright(self):
        print "RFC: Spin right", self.throttle 
        wiringpi.pwmWrite(self.servoleft, self.calcPWM(self.LF, self.LS, self.throttle))
        wiringpi.pwmWrite(self.servoright, self.calcPWM(self.RR, self.RS, self.throttle))
                
    def turnforwardleft(self):
        print "RFC: Turn forward left", self.throttle
        wiringpi.pwmWrite(self.servoleft, self.calcPWM(self.LF, self.LS, self.throttle/2))
        wiringpi.pwmWrite(self.servoright, self.calcPWM(self.RF, self.RS, self.throttle))
    
    def turnforwardright(self):
        print "RFC: Turn forward right", self.throttle
        wiringpi.pwmWrite(self.servoleft, self.calcPWM(self.LF, self.LS, self.throttle))
        wiringpi.pwmWrite(self.servoright, self.calcPWM(self.RF, self.RS, self.throttle/2))
                
    def turnreverseleft(self):
        print "RFC: Turn reverse left", self.throttle
        wiringpi.pwmWrite(self.servoleft, self.calcPWM(self.LR, self.LS, self.throttle/2))
        wiringpi.pwmWrite(self.servoright, self.calcPWM(self.RR, self.RS, self.throttle))
            
    def turnreverseright(self):
        print "RFC: Turn reverse right", self.throttle
        wiringpi.pwmWrite(self.servoleft, self.calcPWM(self.LR, self.LS, self.throttle))
        wiringpi.pwmWrite(self.servoright, self.calcPWM(self.RR, self.RS, self.throttle/2))    
        