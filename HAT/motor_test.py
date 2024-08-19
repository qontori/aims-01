import buildhat

hat = buildhat.Hat()
print(hat.get())
motors = [buildhat.Motor("A"), buildhat.Motor("B")]
color_sensors = [buildhat.ColorSensor("C"), buildhat.ColorSensor("D")]

def SetMotorSpeed(left_speed, right_speed):
    global motors
    motors[0].start(left_speed)
    motors[1].start(right_speed)

def CheckColors(color):
    return color_sensors[0].get_color() == color and color_sensors[1].get_color() == color

def JunctionCheck():
    global JunctionDetected
    if  CheckColors("black"):
        return True
    return False

def LineFollower():
    if CheckColors("white"):
        SetMotorSpeed(50,50)
        return
    if  color_sensors[0].get_color() == "White":
        SetMotorSpeed(25,50)
    else:
        SetMotorSpeed(50,25)

def CheckImage():
    return

def CheckEnd():
    if CheckColors("red"):
        print("Red")
        SetMotorSpeed(0,0)
        return 1
    return 0


def run_motor_test():
    SetMotorSpeed(50,50)
    while not CheckEnd():
        LineFollower()
        if JunctionCheck():
            CheckImage()
