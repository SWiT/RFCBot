# Servo Control
import time
import wiringpi
import pygame

servoleft = 18
servoright = 13

leftforward = 200
rightforward = 50
stop = 150
leftreverse = 50
rightreverse = 200

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

while run:
    for event in pygame.event.get():
        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        if event.type == pygame.JOYBUTTONDOWN:
            #print("Joystick button pressed.")
            for b in range(joystick.get_numbuttons()):
                if joystick.get_button(b) and b%2==0:
                    print "Faster"
                if joystick.get_button(b) and b%2==1:
                    print "Slower"
        if event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")
        if event.type == pygame.JOYAXISMOTION:
            x = joystick.get_axis(0)
            y = joystick.get_axis(1)
            if x == 0 and y == 0:
                print("Stop")
                wiringpi.pwmWrite(servoleft, stop)
                wiringpi.pwmWrite(servoright, stop)
                
            elif x == 0 and y > 0:
                print("Forward")
                wiringpi.pwmWrite(servoleft, leftforward)
                wiringpi.pwmWrite(servoright, rightforward)
                
            elif x == 0 and y < 0:
                print("Reverse")
                wiringpi.pwmWrite(servoleft, leftreverse)
                wiringpi.pwmWrite(servoright, rightreverse)
                
            elif x < 0 and y == 0:
                print("Spin left")
                wiringpi.pwmWrite(servoleft, leftreverse)
                wiringpi.pwmWrite(servoright, rightforward)
            elif x > 0 and y == 0:
                print("Spin right")
                wiringpi.pwmWrite(servoleft, leftforward)
                wiringpi.pwmWrite(servoright, rightreverse)
                
            elif x < 0 and y > 0:
                print("Forward left")
            elif x > 0 and y > 0:
                print("Forward right")
                
            elif x < 0 and y < 0:
                print("Reverse left")
            elif x > 0 and y < 0:
                print("Reverse right")
                
    time.sleep(delay_period)

pygame.joystick.quit()
print "exit."

