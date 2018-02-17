# Servo Control
import time
import wiringpi
import pygame

servoleft = 18
servoright = 13

leftforward = 50
leftstop = 148
leftreverse = -50

rightforward = -50
rightstop = 147
rightreverse = 50

def calcSpeed(direction, stop, throttle):
    return int((direction * throttle) + stop)


# use 'GPIO naming'
wiringpi.wiringPiSetupGpio()

# set #18 to be a PWM output
wiringpi.pinMode(servoleft, wiringpi.GPIO.PWM_OUTPUT)
wiringpi.pinMode(servoright, wiringpi.GPIO.PWM_OUTPUT)

# set the PWM mode to milliseconds stype
wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)

# divide down clock
wiringpi.pwmSetClock(192)
wiringpi.pwmSetRange(2000)

run = True

pygame.init()
pygame.joystick.init()


joystickcount = pygame.joystick.get_count()
print(str(joystickcount)+" Joysticks")
if joystickcount < 1:
    run = False
else:    
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(str(joystick.get_numbuttons())+" Buttons")
    
delay_period = 0.01
throttle = 0.40
accel = 0.05

while run:
    for event in pygame.event.get():
        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        if event.type == pygame.JOYBUTTONDOWN:
            #print("Joystick button pressed.")
            for b in range(joystick.get_numbuttons()):
                if joystick.get_button(b) and b%2==0:
                    throttle = throttle + accel
                    if throttle > 1:
                        throttle = 1
                    print "Faster", throttle
                    
                if joystick.get_button(b) and b%2==1:
                    throttle = throttle - accel
                    if throttle < 0:
                        throttle = 0
                    print "Slower", throttle
                        
        if event.type == pygame.JOYBUTTONUP:
            #print("Joystick button released.")
            pass
            
        if event.type == pygame.JOYAXISMOTION:
            x = joystick.get_axis(0)
            y = joystick.get_axis(1)
            
            if x == 0 and y == 0:
                print("Stop")
                wiringpi.pwmWrite(servoleft, leftstop)
                wiringpi.pwmWrite(servoright, rightstop)
                
            elif x == 0 and y > 0:
                print "Forward", throttle
                wiringpi.pwmWrite(servoleft, calcSpeed(leftforward, leftstop, throttle))
                wiringpi.pwmWrite(servoright, calcSpeed(rightforward, rightstop, throttle))
                
            elif x == 0 and y < 0:
                print "Reverse", throttle 
                wiringpi.pwmWrite(servoleft, calcSpeed(leftreverse, leftstop, throttle))
                wiringpi.pwmWrite(servoright, calcSpeed(rightreverse, rightstop, throttle))
                
            elif x < 0 and y == 0:
                print "Spin left", throttle
                wiringpi.pwmWrite(servoleft, calcSpeed(leftreverse, leftstop, throttle))
                wiringpi.pwmWrite(servoright, calcSpeed(rightforward, rightstop, throttle))
            
            elif x > 0 and y == 0:
                print "Spin right", throttle 
                wiringpi.pwmWrite(servoleft, calcSpeed(leftforward, leftstop, throttle))
                wiringpi.pwmWrite(servoright, calcSpeed(rightreverse, rightstop, throttle))
                
            elif x < 0 and y > 0:
                print "Forward left", throttle
                wiringpi.pwmWrite(servoleft, calcSpeed(leftforward, leftstop, throttle/2))
                wiringpi.pwmWrite(servoright, calcSpeed(rightforward, rightstop, throttle))
                
            elif x > 0 and y > 0:
                print "Forward right", throttle
                wiringpi.pwmWrite(servoleft, calcSpeed(leftforward, leftstop, throttle))
                wiringpi.pwmWrite(servoright, calcSpeed(rightforward, rightstop, throttle/2))
                
            elif x < 0 and y < 0:
                print "Reverse left", throttle
                wiringpi.pwmWrite(servoleft, calcSpeed(leftreverse, leftstop, throttle/2))
                wiringpi.pwmWrite(servoright, calcSpeed(rightreverse, rightstop, throttle))
            
            elif x > 0 and y < 0:
                print "Reverse right", throttle
                wiringpi.pwmWrite(servoleft, calcSpeed(leftreverse, leftstop, throttle))
                wiringpi.pwmWrite(servoright, calcSpeed(rightreverse, rightstop, throttle/2))
                
    time.sleep(delay_period)

pygame.joystick.quit()
print "exit."

