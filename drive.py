# Robot Fight Club driving script.
print "RFC: launching drive.py."

import time
import wiringpi
import pygame

import rfcbot

bot = rfcbot.RFCBot()

drivehat = 0        # The joystick hat used to drive.
driveaxislr = 0     # The Left and Right joystick axis.
driveaxisfb = 1     # The Forwards and Backwards joystick axis.

driveaxisL = 1     # The Forwards and Backwards joystick axis.
driveaxisR = 3     # The Forwards and Backwards joystick axis.

waiting_period = 1.0
delay_period = 0.01


# Initialize Pygame
pygame.init()

# Initialize any joysticks
pygame.joystick.init()
# If no joystick then wait.
joystickcount = pygame.joystick.get_count()
if joystickcount < 1:
    print "RFC: Waiting for Joystick..."
while joystickcount < 1:
    pygame.joystick.quit()
    time.sleep(waiting_period)
    pygame.joystick.init()
    joystickcount = pygame.joystick.get_count()

# Connect to the first joystick.    
joystick = pygame.joystick.Joystick(0)
joystick.init()
print("RFC: Joystick(0) "+str(joystick.get_numbuttons())+" Buttons")


def hatToDrive(x, y):
    if x == 0 and y == 0:
        bot.stop()
    elif x == 0 and y > 0:
        bot.forward()        
    elif x == 0 and y < 0:
        bot.reverse()
    elif x < 0 and y == 0:
        bot.spinleft()
    elif x > 0 and y == 0:
        bot.spinright()
    elif x < 0 and y > 0:
        bot.turnforwardleft()
    elif x > 0 and y > 0:
        bot.turnforwardright()
    elif x < 0 and y < 0:
        bot.turnreverseleft()
    elif x > 0 and y < 0:
        bot.turnreverseright()
    
    
run = True
while run:
    for event in pygame.event.get():
        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        # Button Down
        if event.type == pygame.JOYBUTTONDOWN:
            for b in range(joystick.get_numbuttons()):
                if joystick.get_button(b):
                    print "RFC: Button", b, "Down"
                    
        # Button Up                
        if event.type == pygame.JOYBUTTONUP:
            for b in range(joystick.get_numbuttons()):
                if joystick.get_button(b):
                    print "RFC: Button", b, "Down"
                    
        # Hat Motion
        if event.type == pygame.JOYHATMOTION:
            for h in range(joystick.get_numhats()):
                hat = joystick.get_hat(h)
                print "RFC: HAT ", h, hat
                x = hat[0]
                y = hat[1]
                hatToDrive(x, y)
                
        # Axis Motion    
        if event.type == pygame.JOYAXISMOTION:
            axes = ""
            for a in range(joystick.get_numaxes()):
                axes += str(joystick.get_axis(a)) + " "
            print "RFC: AXES ", axes
            
            leftspeed = -1.0 * joystick.get_axis(driveaxisL)
            rightspeed = -1.0 * joystick.get_axis(driveaxisR)
            bot.setServos(leftspeed, rightspeed)
            
                
    time.sleep(delay_period)

pygame.joystick.quit()
print "RFC: drive.py exit."

