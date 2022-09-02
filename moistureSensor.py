import time
# from numpy import random
import serial
import json
import serial.tools.list_ports as serial_ports
from typing import Final

DEBUG: Final[int] = 1

"""
1- controllare se ci sono arduino collegati
2- se ce ne sono, faccio segliere, quando ce ne è uno solo selezione quello
3- instauro una connessione con l'arduino (invio e ricevo)
4- quanti dati da leggere
5- porte da selezionare
6- lettura dati
"""

# classe per gestire il rilevamente dati da parte di un arduino
# con installati dei sensori di umidità del terreno


class SoilMoistureSensor:
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

        conn = self.Connection(self.serialInst, 9600, self.portSelected)
        if (conn == 0):
            print("Connessione non riuscita")
            return
        print("Connessione stabilita")

        self.totalRead = self.nCount = self.NumberOfData()
        self.sensToRead = self.SenAvailable()
        self.result = self.ReadArduinoData(
            self.serialInst, len(self.sensToRead), self.nCount)

        return 0

    # verifica la connessione con l'arduino
    def Connection(self, inst, baud, port):

        def write_read(msg):
            inst.write(bytes(msg, 'utf-8'))
            time.sleep(0.05)
            data = inst.readline()
            line = data.decode('utf').rstrip('\n')
            return int(line)

        inst.baudrate = baud
        inst.port = port
        inst.open()

        time.sleep(0.5)
        value = 0
        while True:
            if inst.in_waiting:
                fl_data = inst.readline()
                f_line = fl_data.decode('utf').rstrip('\r\n')
                # print(f_line)
                if (f_line == "Booting..."):
                    break
                else:
                    inst.close()
                    return value

        time.sleep(0.5)
        value = write_read("hello world")
        # print(value)
        inst.close()
        return value

    # ritorna il numero di arduino connessi al pc
    def GetPortsNumber(self):
        return serial_ports.comports()

    # ritorna il risultato dei dati raccolti
    def GetResults(self):
        return self.result

    # ritorna un array con i sensori che sono stati usati dall'arduino
    def GetUsedSensors(self):
        return self.sensToRead

    # permette di scegliere la porta sulla quale
    # interfacciarsi con l'arduino nel caso ci sia solo un arduino connesso
    # verrà automaticamente scelta l'unica porta disponibile
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
            print(
                "\nSelezionata in automatico l'unica porta disponibile\n")
            return self.FindPort(str(portList[0]))

    # ritorna il nome della porta, cambia a seconda del sistema operativo
    def FindPort(self, val):
        type = val[0:3]

        if (type == "COM"):
            # windows only
            return val[0:5]
        else:
            # mac os / linux
            return val[0:20]

    # chiede all'utente quanti dati vuole raccogliere dai sensori
    def NumberOfData(self):
        while 1:
            n = input(
                "\nInserisci il numero di righe di dati che vuoi prendere\n")
            try:
                return int(n)
            except:
                print("\nInserisci un valore numerico intero")

    # ritorna un array con i sensori usati dal dispositivo
    def SenAvailable(self):
        if (DEBUG == 1):
            return [0, 1, 2, 3, 4, 5]
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

    # legge dalla seriale dell'arduino i valori che questo vi ci scrive
    def ReadArduinoData(self, inst, nSens, n):
        inst.open()
        data = []
        print("\nElenco dati estrapolati:\n")
        while True:
            if inst.in_waiting:
                packet = inst.readline()
                serial_line = packet.decode('utf').rstrip('\n')
                try:
                    line = json.loads(serial_line)
                    print(serial_line)
                    if (len(line) == nSens):
                        data.append(line)
                        n -= 1
                    if n % 10 == 0:
                        print("\nData left: " + str(n) + "\n")
                except:
                    pass

            if n == 0:
                break

        inst.close()
        return data
