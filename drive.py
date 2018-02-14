# Servo Control
import time
import wiringpi
import pygame

servoleft = 18
servoright = 13

leftforward = 50
rightforward = 200
stop = 150
leftreverse = 200
rightreverse = 50

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
    
delay_period = 0.01

while run:
    for event in pygame.event.get():
        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        if event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        if event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")
    #wiringpi.pwmWrite(stop, 150)
    #wiringpi.pwmWrite(stop, 150)
    #time.sleep(delay_period)

pygame.joystick.quit()
print "exit."

