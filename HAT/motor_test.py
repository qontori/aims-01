import buildhat

hat = buildhat.Hat()
print(hat.get())
motors = buildhat.MotorPair("A","B")
color_sensors = [buildhat.ColorSensor("C"), buildhat.ColorSensor("D")]

def SetMotorSpeed(left_speed, right_speed):
    global motors
    motors.start(-left_speed, right_speed)

def CheckColors(color):
    return color_sensors[0].get_color() == color and color_sensors[1].get_color() == color

def JunctionCheck():
    global JunctionDetected
    if  CheckColors("black"):
        return True
    return False

def LineFollower():
    #print("speed : " + str(motors.get_speed()) + " : " + str(motors.get_speed()))
    if CheckColors("white") or CheckColors("black"):
        SetMotorSpeed(5,5)
        return
    if  color_sensors[0].get_color() == "white":
        SetMotorSpeed(5,2.5)
    else:
        SetMotorSpeed(2.5,5)

def CheckImage():
    return

def CheckEnd():
    if CheckColors("red"):
        print("Red")
        SetMotorSpeed(0,0)
        return 1
    return 0


def run_motor_test():
    SetMotorSpeed(5,5)
    while not CheckEnd():
        LineFollower()
        if JunctionCheck():
            CheckImage()

run_motor_test()