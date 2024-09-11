#I have no idea if anything here works, but we'll see
import motor, math, runloop, sys
from hub import port, motion_sensor

class CoordindateSystem():
    def __init__(self, width, height, *, port1=port.A, port2=port.B, wheel_diameter=8.8, wheel_distance=8):
        motion_sensor.reset_yaw(0)
        self.width = width
        self.height = height
        self.port1 = port1
        self.port2 = port2
        self.wheel_diameter = wheel_diameter
        self.wheel_circumference = wheel_diameter * math.pi
        self.wheel_distance = wheel_distance
        self.drivingbase_360_degrees_turn_circumference = self.wheel_distance * math.pi
        self.x = 0
        self.y = 0
        
    def rotateToAngle(self, angle, speed=100):
        self.fractionOf360Degrees = (angle + (motion_sensor.tilt_angles()[0] * -0.1)) / 360
        self.degrees = (self.drivingbase_360_degrees_turn_circumference * self.fractionOf360Degrees / self.wheel_circumference) * 360
        runloop.run(motor.run_for_degrees(self.port1, round(self.degrees), speed), motor.run_for_degrees(self.port2, round(self.degrees), speed))

    def moveForDistance(self, distance, speed=300):
        self.degrees_per_cm = 360 / self.wheel_circumference
        runloop.run(motor.run_for_degrees(self.port1, round(distance*self.degrees_per_cm), speed), motor.run_for_degrees(self.port2, round(distance*self.degrees_per_cm), speed))
        
    def goTo(self, target_x, target_y, speed=300):
        if target_x > self.width or target_y > self.height or target_x < 0 or target_y < 0:
            print("Invalid Coordinates")
            continue
            #if it still doesn't work, just remove the entire if-structure
        
        self.difference_x = target_x - self.x
        self.difference_y = target_y - self.y
        
        self.distance = math.sqrt(self.difference_x**2 + self.difference_y**2)
        self.angle = math.degrees(math.atan2(self.difference_y, self.difference_x))

        rotateToAngle(self.angle, speed=speed)
        moveForDistance(self.distance, speed=speed)

        self.x = target_x
        self.y = target_y

b = CoordinateSystem(200, 100)
b.goTo(100, 50)


