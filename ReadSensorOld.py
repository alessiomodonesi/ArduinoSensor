from numpy import random
import serial
import os
import json
import serial.tools.list_ports
from typing import Final

DEBUG: Final[int] = 0
ARDUINO: Final[str] = "ArduinoMkr1310"


def findPort(val):
    type = val[0:3]

    if (type == "COM"):
        # windows only
        return val[0:5]
    else:
        # mac os / linux
        return val[0:20]


def portSelection():
    print("\nElenco porte utilizzabili:")
    ports = serial.tools.list_ports.comports()
    portList = []

    # mostra tutte le porte utilizzabili
    i = 0
    for onePort in ports:
        portList.append(str(onePort))
        print(str(i) + " -> " + str(onePort))
        i += 1

    while 1:
        index = input("\nSeleziona la porta da usare\n")
        try:
            index = int(index)
            return findPort(str(portList[index]))
        except:
            print("\nPorta non trovata")


def getNumberOfData():
    while 1:
        n = input("\nInserisci il numero di righe di dati che vuoi prendere\n")
        try:
            return int(n)
        except:
            print("\nInserisci un valore numerico intero")


def getSenAvailable():
    while 1:
        availableSensors = [0, 1, 2, 3, 4, 5]
        r = input(
            "\nInserisci il numero corrispondente dei sensori separati da una virgola\n")
        if (r.lower() == "all"):
            rSens = availableSensors
            break
        else:
            try:
                rSens = r.split(',')
                for i in range(len(rSens)):
                    rSens[i] = int(rSens[i])
                    availableSensors.remove(rSens[i])
                break
            except:
                print(
                    "\nValore non corretto\nOppure hai inserito il valore dello stesso sensore più di una volta")

    # print(rSens)
    return rSens


def getRandomValue():
    # generate some integers
    value = random.randint(196, 516, size=(len(sensToRead)))
    value = value.tolist()

    print(value)
    # print(type(value))
    return value


def formatData(array):
    for i in range(len(array)):
        array[i] = json.loads(array[i])
    print("Formatting completed")
    return array


data = []

dataType = input("Tipo di valore che vuoi registrare?\n")

totalRead = nCount = getNumberOfData()
sensToRead = getSenAvailable()

if (DEBUG == 0):
    typePort = portSelection()

    serialInst = serial.Serial()

    serialInst.baudrate = 9600
    # serialInst.port = "COM3"
    # serialInst.port = "/dev/cu.usbmodem1101"
    serialInst.port = typePort
    serialInst.open()

print("\nElenco dati estrapolati:\n")

while True:
    if (DEBUG == 0):
        if serialInst.in_waiting:
            packet = serialInst.readline()
            serial_line = packet.decode('utf').rstrip('\n')
            try:
                line = json.loads(serial_line)
                print(serial_line)
                if (len(line) == len(sensToRead)):
                    data.append(line)
                    nCount -= 1
                if nCount % 10 == 0:
                    print("\nData left: " + str(nCount) + "\n")
            except:
                pass
    else:
        data.append(getRandomValue())
        nCount -= 1
        if nCount % 10 == 0:
            print("\nData left: " + str(nCount) + "\n")

    if nCount == 0:
        break

if (DEBUG == 0):
    serialInst.close()
    # data = formatData(data)
# print(data)

sommaSingleCol = {
    "sen0": 0, "sen1": 0,
    "sen2": 0, "sen3": 0,
    "sen4": 0, "sen5": 0
}
mediaSingleCol = {
    "sen0": 0, "sen1": 0,
    "sen2": 0, "sen3": 0,
    "sen4": 0, "sen5": 0
}

for i in range(len(data)):
    for j in range(len(sensToRead)):
        sommaSingleCol["sen" +
                       str(sensToRead[j])] += int(data[i][sensToRead[j]])

for i in range(len(sensToRead)):
    mediaSingleCol["sen" +
                   str(sensToRead[i])] = int(sommaSingleCol[
                       "sen" + str(sensToRead[i])] / totalRead)

somma = 0
media = 0

somma = sommaSingleCol["sen0"] + sommaSingleCol["sen1"] + sommaSingleCol["sen2"] + \
    sommaSingleCol["sen3"] + sommaSingleCol["sen4"] + sommaSingleCol["sen5"]

print("Somma : " + str(somma))
media = int(somma / (len(sensToRead)*totalRead))
print("Media : " + str(media))

# crea le cartelle
os.makedirs(ARDUINO + "/calc", exist_ok=True)
os.makedirs(ARDUINO + "/data", exist_ok=True)


j = open(ARDUINO + "/data/sensorsData_" + str(dataType) + ".json", "w")
j.write(str(json.dumps(data)))
j.close()

d = open(ARDUINO + "/calc/calcolo_" + str(dataType) + ".txt", "w")
d.write(
    "Somma Totale: " + str(somma) + "\n" +
    "Media Totale: " + str(media) + "\n\n" +

    "Somma A0: " + str(sommaSingleCol["sen0"]) + "\n" +
    "Somma A1: " + str(sommaSingleCol["sen1"]) + "\n" +
    "Somma A2: " + str(sommaSingleCol["sen2"]) + "\n" +
    "Somma A3: " + str(sommaSingleCol["sen3"]) + "\n" +
    "Somma A4: " + str(sommaSingleCol["sen4"]) + "\n" +
    "Somma A5: " + str(sommaSingleCol["sen5"]) + "\n\n" +

    "Media A0: " + str(mediaSingleCol["sen0"]) + "\n" +
    "Media A1: " + str(mediaSingleCol["sen1"]) + "\n" +
    "Media A2: " + str(mediaSingleCol["sen2"]) + "\n" +
    "Media A3: " + str(mediaSingleCol["sen3"]) + "\n" +
    "Media A4: " + str(mediaSingleCol["sen4"]) + "\n" +
    "Media A5: " + str(mediaSingleCol["sen5"]) + "\n"
)

d.close()
