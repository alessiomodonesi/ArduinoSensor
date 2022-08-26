import serial
import json
import serial.tools.list_ports


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
        index = int(index)
        try:
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


data = []

dataType = input("Tipo di valore che vuoi registrare?\n")

totalRead = nCount = getNumberOfData()
typePort = portSelection()
# nSensors = getSenAvailable()

serialInst = serial.Serial()

serialInst.baudrate = 9600
# serialInst.port = "COM3"
# serialInst.port = "/dev/cu.usbmodem1101"
serialInst.port = typePort
serialInst.open()

print("\nElenco dati estrapolati:\n")

while True:
    if serialInst.in_waiting:
        packet = serialInst.readline()
        serial_line = packet.decode('utf').rstrip('\n')
        try:
            line = json.loads(serial_line)
            print(line)
            data.append(line)
            nCount -= 1
            if nCount % 10 == 0:
                print("\nData left: " + str(nCount) + "\n")
        except:
            pass
    if nCount == 0:
        break

serialInst.close()
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
    sommaSingleCol["sen0"] += int(data[i][0])
    sommaSingleCol["sen1"] += int(data[i][1])
    sommaSingleCol["sen2"] += int(data[i][2])
    sommaSingleCol["sen3"] += int(data[i][3])
    sommaSingleCol["sen4"] += int(data[i][4])
    sommaSingleCol["sen5"] += int(data[i][5])

mediaSingleCol["sen0"] = int(sommaSingleCol["sen0"] / totalRead)
mediaSingleCol["sen1"] = int(sommaSingleCol["sen1"] / totalRead)
mediaSingleCol["sen2"] = int(sommaSingleCol["sen2"] / totalRead)
mediaSingleCol["sen3"] = int(sommaSingleCol["sen3"] / totalRead)
mediaSingleCol["sen4"] = int(sommaSingleCol["sen4"] / totalRead)
mediaSingleCol["sen5"] = int(sommaSingleCol["sen5"] / totalRead)

somma = 0
media = 0

somma = sommaSingleCol["sen0"] + sommaSingleCol["sen1"] + sommaSingleCol["sen2"] + \
    sommaSingleCol["sen3"] + sommaSingleCol["sen4"] + sommaSingleCol["sen5"]

print("Somma : " + str(somma))
media = int(somma / (6*totalRead))
print("Media : " + str(media))

j = open("sensorsData_" + str(dataType) + ".json", "w")
j.write(str(json.dumps(data)))
j.close()

d = open("calcolo_" + str(dataType) + ".txt", "w")
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
