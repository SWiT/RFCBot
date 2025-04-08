# Robot Fight Club driving script.
from __future__ import print_function

print("RFC: launching drive.py.")

import time, datetime, sys
import wiringpi
import pygame

import rfcbot

bot = rfcbot.RFCBot()

delay_period = 0.01

now = datetime.datetime.now()
timer_mpu = now
timer_output = now

cfg = bot.config
accel_data = {}
gyro_data = {}
    
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
            if bot.joystick.get_button(cfg["btnHotkey"]):
                if bot.joystick.get_button(cfg["btnExit"]):
                    run = False
                elif bot.joystick.get_button(cfg["btnCalMPU"]):
                    bot.calibrateMPU()
                else:
                    y = 0
                    bot.calibrateServo(y)


        # Button Up                
        if event.type == pygame.JOYBUTTONUP:
            print("RFC: Button "+str(event.button)+" Up" )

         
        # Hat Motion
        if event.type == pygame.JOYHATMOTION:
            for h in range(bot.joystick.get_numhats()):
                hat = bot.joystick.get_hat(h)
                print("RFC: HAT ", h, hat, bot.joystick.get_button(cfg["btnHotkey"]))
                if bot.joystick.get_button(cfg["btnHotkey"]):
                    y = hat[1]
                    bot.calibrateServo(y)
                    bot.stop()
                else:
                    x = hat[0]
                    y = hat[1]
                    bot.hatToDrive(x, y)

                
        # Axis Motion    
        if event.type == pygame.JOYAXISMOTION:
            #print(event)
            if event.axis==cfg["driveAxisL"] or event.axis==cfg["driveAxisR"]:
                print("RFC: AXIS ", event.axis, " VALUE", event.value)
                leftspeed = -1.0 * bot.joystick.get_axis(cfg["driveAxisL"])
                rightspeed = 1.0 * bot.joystick.get_axis(cfg["driveAxisR"])
                print("RFC: leftspeed ", leftspeed, " rightspeed", rightspeed)
                bot.setServos(leftspeed, rightspeed)
            
    # Check the MPU
    if now > timer_mpu:
        # Read the sensor data
        gyro_data = bot.get_gyro_data()
        accel_data = bot.get_accel_data()
        timer_mpu = now + datetime.timedelta(milliseconds=2)
    
    # Output
    if now > timer_output:
        #print(now)
        #print("A:", accel_data)
        #print("G:", gyro_data)
        #print()
        timer_output = now + datetime.timedelta(seconds=5)
        
    time.sleep(delay_period)

pygame.joystick.quit()
print("*******************")
print("RFC: drive.py exit.")
print("*******************")



