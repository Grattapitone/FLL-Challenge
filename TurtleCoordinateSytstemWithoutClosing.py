import turtle
import math

turtle.penup()
turtle.setpos(0, 0)
turtle.pendown()

target_x = int(input("target x? "))
target_y = int(input("target y? "))
    
def move_to_target(target_x, target_y):
    difference_x = target_x - turtle.xcor()
    difference_y = target_y - turtle.ycor()
    
    distance = math.sqrt(difference_x**2 + difference_y**2)
    angle = math.degrees(math.atan2(difference_y, difference_x))
    
    turtle.setheading(angle)
    turtle.forward(distance)

move_to_target(target_x, target_y)

while not input("exit? "):
    pass
