import os
import json
from typing import Final
from moistureSensor import SoilMoistureSensor

# Nome del dispositivo (per creare una cartella separata)
ARDUINO: Final[str] = "ArduinoMkr1310"

mSensor = SoilMoistureSensor()
# se ci sono stati degli errori durante l'esecuzione il programma termina
if (mSensor.Start() == None):
    exit()

filename = input("Come vuoi salvare i dati?\n")

data = mSensor.GetResults()
nData = len(data)
sensorsUsed = mSensor.GetUsedSensors()

sommaSensori = {
    "sen0": 0, "sen1": 0,
    "sen2": 0, "sen3": 0,
    "sen4": 0, "sen5": 0
}
mediaSensori = {
    "sen0": 0, "sen1": 0,
    "sen2": 0, "sen3": 0,
    "sen4": 0, "sen5": 0
}

for i in range(len(data)):
    for j in range(len(sensorsUsed)):
        sommaSensori["sen" +
                     str(sensorsUsed[j])] += int(data[i][sensorsUsed[j]])

for i in range(len(sensorsUsed)):
    mediaSensori["sen" + str(sensorsUsed[i])] = int(sommaSensori[
        "sen" + str(sensorsUsed[i])] / nData)

sommaTot = 0
mediaTot = 0

sommaTot = sommaSensori["sen0"] + sommaSensori["sen1"] + sommaSensori["sen2"] + \
    sommaSensori["sen3"] + sommaSensori["sen4"] + sommaSensori["sen5"]

print("Somma : " + str(sommaTot))
mediaTot = int(sommaTot / (len(sensorsUsed)*nData))
print("Media : " + str(mediaTot))

# crea le cartelle
os.makedirs(ARDUINO + "/calc", exist_ok=True)
os.makedirs(ARDUINO + "/data", exist_ok=True)


j = open(ARDUINO + "/data/sensorsData_" + str(filename) + ".json", "w")
j.write(str(json.dumps(data)))
j.close()

d = open(ARDUINO + "/calc/calcolo_" + str(filename) + ".txt", "w")
d.write(
    "Somma Totale: " + str(sommaTot) + "\n" +
    "Media Totale: " + str(mediaTot) + "\n\n" +

    "Somma A0: " + str(sommaSensori["sen0"]) + "\n" +
    "Somma A1: " + str(sommaSensori["sen1"]) + "\n" +
    "Somma A2: " + str(sommaSensori["sen2"]) + "\n" +
    "Somma A3: " + str(sommaSensori["sen3"]) + "\n" +
    "Somma A4: " + str(sommaSensori["sen4"]) + "\n" +
    "Somma A5: " + str(sommaSensori["sen5"]) + "\n\n" +

    "Media A0: " + str(mediaSensori["sen0"]) + "\n" +
    "Media A1: " + str(mediaSensori["sen1"]) + "\n" +
    "Media A2: " + str(mediaSensori["sen2"]) + "\n" +
    "Media A3: " + str(mediaSensori["sen3"]) + "\n" +
    "Media A4: " + str(mediaSensori["sen4"]) + "\n" +
    "Media A5: " + str(mediaSensori["sen5"]) + "\n"
)

d.close()
