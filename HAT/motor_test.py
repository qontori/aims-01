import buildhat

hat = buildhat.Hat()
print(hat.get())
motor_a = buildhat.Motor("A")
motor_a.run_for_seconds(5, speed=50)