import os
import json
from typing import Final
from moistureSensor import SoilMoistureSensor

ARDUINO: Final[str] = "ArduinoMkr1310"


mSensor = SoilMoistureSensor()
if (mSensor.Start() == None):
    exit()

filename = input("Come vuoi salvare i dati?\n")

data = mSensor.GetResults()
nData = len(data)
sensorsUsed = mSensor.GetUsedSensors()

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
    for j in range(len(sensorsUsed)):
        sommaSingleCol["sen" +
                       str(sensorsUsed[j])] += int(data[i][sensorsUsed[j]])

for i in range(len(sensorsUsed)):
    mediaSingleCol["sen" +
                   str(sensorsUsed[i])] = int(sommaSingleCol[
                       "sen" + str(sensorsUsed[i])] / nData)

somma = 0
media = 0

somma = sommaSingleCol["sen0"] + sommaSingleCol["sen1"] + sommaSingleCol["sen2"] + \
    sommaSingleCol["sen3"] + sommaSingleCol["sen4"] + sommaSingleCol["sen5"]

print("Somma : " + str(somma))
media = int(somma / (len(sensorsUsed)*nData))
print("Media : " + str(media))

# crea le cartelle
os.makedirs(ARDUINO + "/calc", exist_ok=True)
os.makedirs(ARDUINO + "/data", exist_ok=True)


j = open(ARDUINO + "/data/sensorsData_" + str(filename) + ".json", "w")
j.write(str(json.dumps(data)))
j.close()

d = open(ARDUINO + "/calc/calcolo_" + str(filename) + ".txt", "w")
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
