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

pygame.init()
pygame.key.set_repeat(100, 100)

delay_period = 0.01
run = True
while run:
    for event in pygame.event.get():
        print "Event!"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                print 'go forward'
            if event.key == pygame.K_s:
                print 'go backward'
        if event.type == pygame.KEYUP:
            print 'stop'
    #wiringpi.pwmWrite(stop, 150)
    #wiringpi.pwmWrite(stop, 150)
    #time.sleep(delay_period)
    
print "exit."
		