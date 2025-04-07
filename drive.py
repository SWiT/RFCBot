# Robot Fight Club driving script.
from __future__ import print_function

print("RFC: launching drive.py.")

import time, datetime, sys
import wiringpi
import pygame


import rfcbot

bot = rfcbot.RFCBot()

drivehat = 0        # The joystick hat used to drive.
driveaxislr = 0     # The Left and Right joystick axis.
driveaxisfb = 1     # The Forwards and Backwards joystick axis.

driveaxisL = 1     # The Forwards and Backwards joystick axis.
driveaxisR = 3     # The Forwards and Backwards joystick axis.

# Calibration buttons
cbhotkey = 12
cbLF = 6
cbLS = 4
cbLR = 8
cbRF = 7
cbRS = 0
cbRR = 9
cbMPU = 3
exitButton = 11

waiting_period = 1.0
delay_period = 0.01

        
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
    time.sleep(waiting_period)
    pygame.joystick.init()
    joystickcount = pygame.joystick.get_count()

# Connect to the first joystick.    
joystick = pygame.joystick.Joystick(0)
joystick.init()
print("RFC: Joystick(0) "+str(joystick.get_numbuttons())+" Buttons")


now = datetime.datetime.now()
timer_mpu = now

    
run = True
while run:
    then = now
    now = datetime.datetime.now()
    time_diff = now - then

    for event in pygame.event.get():
        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        # Button Down
        if event.type == pygame.JOYBUTTONDOWN:
            print("RFC: Button "+str(event.button)+" Down")
            if joystick.get_button(cbhotkey):
                if joystick.get_button(exitButton):
                    run = False
                elif joystick.get_button(cbMPU):
                    bot.calibrateMPU()
                else:
                    y = 0
                    bot.calibrateServo(y)


        # Button Up                
        if event.type == pygame.JOYBUTTONUP:
            print("RFC: Button "+str(event.button)+" Up" )

         
        # Hat Motion
        if event.type == pygame.JOYHATMOTION:
            for h in range(joystick.get_numhats()):
                hat = joystick.get_hat(h)
                print("RFC: HAT ", h, hat, joystick.get_button(cbhotkey))
                if joystick.get_button(cbhotkey):
                    y = hat[1]
                    bot.calibrateServo(y)
                    bot.stop()
                else:
                    x = hat[0]
                    y = hat[1]
                    bot.hatToDrive(x, y)

                
        # Axis Motion    
        if event.type == pygame.JOYAXISMOTION:
            axes = ""
            for a in range(joystick.get_numaxes()):
                axes += str(joystick.get_axis(a)) + " "
            print("RFC: AXES ", axes)
            leftspeed = -1.0 * joystick.get_axis(driveaxisL)
            rightspeed = -1.0 * joystick.get_axis(driveaxisR)
            bot.setServos(leftspeed, rightspeed)
            
    # Check the MPU
    if now > timer_mpu:
        # Read the sensor data
        #accelerometer_data, gyroscope_data, temperature = read_sensor_data()
        gyroscope_data = bot.mpu6050.get_gyro_data()
        accelerometer_data = bot.mpu6050.get_accel_data()
        
        # Print the sensor data
        #print("A:", accelerometer_data)
        #print("G:", gyroscope_data)
        #print("Temp:", temperature)
        #print("\n")
        
        timer_mpu = now + datetime.timedelta(milliseconds=2)
        
        
    time.sleep(delay_period)

pygame.joystick.quit()
print("*******************")
print("RFC: drive.py exit.")
print("*******************")



