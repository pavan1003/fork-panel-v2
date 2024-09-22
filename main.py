#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

ev3 = EV3Brick()
ev3.speaker.set_speech_options(
    language="en-us", voice="f2", speed=30, pitch=50)
ev3.speaker.set_volume(volume=5, which='_all_')

# Initialize motors and sensor
mainMotorSwitch = Motor(Port.A, Direction.CLOCKWISE)
motorB = Motor(Port.B, Direction.CLOCKWISE)
motorC = Motor(Port.C, Direction.CLOCKWISE)
# motorD = Motor(Port.D, Direction.CLOCKWISE)

switch2 = TouchSensor(Port.S2)
switch3 = TouchSensor(Port.S3)
switch4 = TouchSensor(Port.S4)

# Move motor until stalled to make a default position
mainMotorSwitch.run_until_stalled(speed=-100, then=Stop.HOLD, duty_limit=20)
initialMainMotorAngle = mainMotorSwitch.angle()

# The Inital angle will always me negative as the motor moves reverse.
print("Initial Angle:", initialMainMotorAngle)

mainMotorSwitch.run_target(
    speed=500, target_angle=initialMainMotorAngle + 64, then=Stop.HOLD, wait=True)
# Now, reset the motor's angle to zero after it has reached the physical limit
mainMotorSwitch.reset_angle(0)

# Function to toggle motor between 0 and 60 degrees


def toggle_motor_position():
    angle = mainMotorSwitch.angle()
    print("Current motor ANGLE: ", angle)

    # If the motor is moved away from 0, move it to 60 degrees (ON)
    if (angle >= -8 and angle <= -3) or (angle >= 3 and angle <= 15):
        # if angle > 2 and angle <= 89:
        mainMotorSwitch.run_target(
            speed=500, target_angle=60, then=Stop.BRAKE, wait=True)
        ev3.speaker.play_notes(['C4/8', 'E4/8', 'G4/4'], 300)
        return True

    # If the motor is moved away from 60, move it back to 0 degrees (OFF)
    elif (angle >= 50 and angle <= 57) or (angle >= 63 and angle <= 68):
        mainMotorSwitch.run_target(
            speed=-500, target_angle=0, then=Stop.BRAKE, wait=True)
        ev3.speaker.play_notes(['G4/8', 'E4/8', 'C4/4'], 120)
        return False

    # Motor is either at 0 or 60 degrees
    return angle >= 59 or angle <= 62


# Write your program here.
ev3.speaker.beep()

# Main loop to continuously check the motor switch and sensor
while True:
    # Check if the motor is in the ON position (60 degrees)
    motor_on = toggle_motor_position()

    if motor_on:
        # If the motor is ON, check if the touch sensor is pressed
        if switch2.pressed():
            # Print message and play a beep when pressed
            print("Switch is pressed!")
            ev3.speaker.beep()
    else:
        # Motor is OFF, no actions taken
        pass

    # Small delay to avoid overloading the CPU
    wait(100)
