import os
import json
from typing import Final
from arduinoCon import ArduinoConnection

ARDUINO: Final[str] = "ArduinoMkr1310"


ardC = ArduinoConnection()
ardC.Start()
