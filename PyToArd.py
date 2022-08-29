import serial
import time

arduino = serial.Serial(port='COM3', baudrate=9600)

time.sleep(3)
print("Collega l'arduino")


def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    line = data.decode('utf').rstrip('\n')
    return line


"""
while True:
    num = input("Enter something: ")
    if (num.lower() == "close"):
        break
    value = write_read(num)
    print(value)
"""

time.sleep(3)
value = write_read("hello world")
print(value)

arduino.close()
