from numpy import random
import serial
import json
# import serial.tools.list_ports
import serial.tools.list_ports as serial_ports
from typing import Final

DEBUG: Final[int] = 0

"""
1- controllare se ci sono arduino collegati
2- se ce ne sono, faccio segliere, quando ce ne è uno solo selezione quello
3- instauro una connessione con l'arduino (invio e ricevo)
4- nome dei file
5- quanti dati da leggere
6- porte da selezionare
7- lettura dati
8- elaborazione dati
"""


class ArduinoConnection:
    def __init__(self):
        self.result = None
        self.ports = None
        self.totalRead = None
        self.nCount = None
        self.sensToRead = None
        self.portSelected = None
        self.serialInst = serial.Serial()

    def Start(self):
        self.ports = self.GetPortsNumber()
        if (len(self.ports) == 0):
            print("Non c'è nessun dispositivo collegato!\nCollega un Arduino e riprova")
            return
        self.portSelected = self.PortSelection(self.ports)
        self.Connection(9600, self.portSelected)

    def Connection(self, baud, port):
        self.serialInst.baudrate = baud
        self.serialInst.port = port
        self.serialInst.open()

    def GetPortsNumber(self):
        return serial_ports.comports()

    def PortSelection(self, ports):
        print("\nElenco porte utilizzabili:")
        portList = []
        i = 0
        # mostra tutte le porte utilizzabili
        for onePort in ports:
            portList.append(str(onePort))
            print(str(i) + " -> " + str(onePort))
            i += 1
        if (len(ports) > 1):
            while 1:
                index = input("\nSeleziona la porta da usare\n")
                try:
                    index = int(index)
                    return self.FindPort(str(portList[index]))
                except:
                    print("\nPorta non trovata")
        else:
            return self.FindPort(str(portList[0]))

    def FindPort(self, val):
        type = val[0:3]

        if (type == "COM"):
            # windows only
            return val[0:5]
        else:
            # mac os / linux
            return val[0:20]

    def GetNumberOfData(self):
        while 1:
            n = input(
                "\nInserisci il numero di righe di dati che vuoi prendere\n")
            try:
                return int(n)
            except:
                print("\nInserisci un valore numerico intero")

    def GetSenAvailable(self):
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
        return rSens

    # sens ---> sensToRead
    def GetRandomValue(self, sens):
        # generate some integers
        value = random.randint(196, 516, size=(len(sens)))
        value = value.tolist()

        print(value)
        # print(type(value))
        return value
