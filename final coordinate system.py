from hub import port, motion_sensor
import motor_pair, motor, sys, math

motor_pair.pair(motor_pair.PAIR_1, port.B, port.A)

wheel_diameter = 8.8
wheel_circumference = wheel_diameter * math.pi
degrees_per_centimeter = 360 / wheel_circumference

hub_x, hub_y = 0, 0

def Turn2Angle(angle):
    while -(motion_sensor.tilt_angles()[0] / 10) < angle:
        if round((motion_sensor.tilt_angles()[0]) / 10 + angle) > 50:
            motor_pair.move(motor_pair.PAIR_1,100,velocity = round((motion_sensor.tilt_angles()[0]) / 10 + angle))
        else:
            motor_pair.move(motor_pair.PAIR_1,100,velocity = 50)
    motor_pair.stop(motor_pair.PAIR_1)

Kp = 1.5

def moveForDistance(distance, speed=300):
    degrees = distance * degrees_per_centimeter         # total degrees the motors have to turn

    motor_beg_pos = motor.absolute_position(port.A)     # beginning position of the Motor
    while motor.relative_position(port.A) - motor_beg_pos < degrees:
        motor_pair.move(motor_pair.PAIR_1, round(motion_sensor.tilt_angles()[0]/10 * (100/ 180) * Kp), velocity = speed)
    motor_pair.stop(motor_pair.PAIR_1)

def moveTo(x, y, speed=300):
    global hub_x, hub_y
    distance = math.sqrt((hub_x - x) ** 2 + (hub_y - y) ** 2)
    angle = math.degrees(math.atan2(hub_y - y, hub_x - x))
    Turn2Angle(angle)
    moveForDistance(distance, speed)
    hub_x, hub_y = x, y

moveTo(10, 0)
moveTo(10, 10)
moveTo(0, 10)
moveTo(0, 0)
sys.exit()