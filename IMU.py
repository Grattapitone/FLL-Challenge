from hub import motion_sensor, light_matrix
import sys, time, math, color
from app import display, linegraph

#CALIBRATING ACCELERATION
light_matrix.show_image(light_matrix.IMAGE_NO)

acceleration_offset_right = 0            #robot offset of the acceleration perpendicular to the motordriving direction
acceleration_offset_forward = 0        #robot offset of the acceleration in motordriving direction
measurement_sum_right = 0                #sum of acceleration measurements for the right direction
measurement_sum_forward = 0            #sum of acceleration measurements for the forward direction
for _ in range(5000):
    measurement_sum_right += motion_sensor.acceleration(False)[1]
    measurement_sum_forward += motion_sensor.acceleration(False)[0]
acceleration_offset_right = measurement_sum_right / 5000
acceleration_offset_forward = measurement_sum_forward / 5000
light_matrix.show_image(light_matrix.IMAGE_YES)
#END CALIBRATING

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

start_time = time.ticks_ms()
current_time = time.ticks_ms() - start_time
previous_time = current_time

while current_time < 5000:
    current_time = time.ticks_ms() - start_time
    difference_time = current_time - previous_time

    acceleration_forward = (motion_sensor.acceleration(False)[0] - acceleration_offset_forward)     # milli-g  =  9,81 m/s/s/1000
    velocity_forward = velocity_forward + (acceleration_forward * difference_time)                  # ---> 9,81 m/s /1.000.000
    distance_forward = distance_forward + (velocity_forward * difference_time)                      # ---> 9,81 m / 1.000.000.000
    meters_moved = (distance_forward / 1000000000) * 9.81

    if do_linegraph:
        linegraph.plot(color.RED,current_time,acceleration_forward/1000)
        linegraph.plot(color.BLUE,current_time,(velocity_forward/1000000)*9.81)
        linegraph.plot(color.GREEN,current_time,meters_moved)

    previous_time = current_time

light_matrix.write(str(meters_moved))

time.sleep(3)

sys.exit()