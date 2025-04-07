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

cfg = bot.config
    
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
            axes = ""
            for a in range(bot.joystick.get_numaxes()):
                axes += str(bot.joystick.get_axis(a)) + " "
            print("RFC: AXES ", axes)
            leftspeed = -1.0 * bot.joystick.get_axis(cfg["driveAxisL"])
            rightspeed = -1.0 * bot.joystick.get_axis(cfg["driveAxisR"])
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



