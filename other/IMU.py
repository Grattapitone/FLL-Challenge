from hub import motion_sensor, light_matrix
import sys, time, math, color
from app import display, linegraph

# CALIBRATING ACCELERATION
light_matrix.show_image(light_matrix.IMAGE_NO)

acceleration_offset_right = 0           #robot offset of the acceleration perpendicular to the motordriving direction
acceleration_offset_forward = 0         #robot offset of the acceleration in motordriving direction
measurement_sum_right = 0               #sum of acceleration measurements for the right direction
measurement_sum_forward = 0             #sum of acceleration measurements for the forward direction
for i in range(3000):
    measurement_sum_right += motion_sensor.acceleration(False)[1]
    measurement_sum_forward += motion_sensor.acceleration(False)[0]
acceleration_offset_right = measurement_sum_right / (i+1)
acceleration_offset_forward = measurement_sum_forward / (i+1)
light_matrix.show_image(light_matrix.IMAGE_YES)
#END CALIBRATING

# Determine whether the hub is connected to the app,
# because otherwise, since the linegraph doesn't work, it will stop the program.
do_linegraph = True
try:
    linegraph.clear_all()
    light_matrix.write("app")
except:
    do_linegraph = False
    light_matrix.write("hub")

acceleration_forward = 0
velocity_forward = 0
distance_forward = 0

start_time = time.ticks_ms()                    # ticks_ms is the time since the hub was turned on and we want to start at zero
current_time = time.ticks_ms() - start_time
previous_time = current_time

while current_time < 5000:
    current_time = time.ticks_ms() - start_time
    difference_time = current_time - previous_time

    # The next four lines are for calculating the distance moved in meters by
    # multiplying the acceleration by the time that passed since the last loop
    # We stay in milli-g for now to preserve precision 
    acceleration_forward = (motion_sensor.acceleration(False)[0] - acceleration_offset_forward)     # milli-g  =  9,81 m/s/s/1000
    velocity_forward = velocity_forward + (acceleration_forward * difference_time)                  # ---> 9,81 m/s /1.000.000
    distance_forward = distance_forward + (velocity_forward * difference_time)                      # ---> 9,81 m / 1.000.000.000
    meters_moved = (distance_forward / 1000000000) * 9.81

    if do_linegraph:
        linegraph.plot(color.RED,current_time,acceleration_forward/1000)            # the red curve is the acceleration in g
        linegraph.plot(color.BLUE,current_time,(velocity_forward/1000000)*9.81)     # the blue curve is the velocity in m/s
        linegraph.plot(color.GREEN,current_time,meters_moved)                       # the green curve is the displacement in meters

    previous_time = current_time        # the time we need to subtract from current_time next loop to get a difference

light_matrix.write(str(meters_moved))

time.sleep(3)

sys.exit()