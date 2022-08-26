#include <SigFox.h>

bool value_to_send = true;

#define DEBUG 1

void setup() {

  if (DEBUG){
    Serial.begin(9600);
    while (!Serial) {};
  }

  if (!SigFox.begin()) {
    if (DEBUG){
      Serial.println("Sigfox module unavailable !");
    }
    return;
  }

  if (DEBUG){
    SigFox.debug();
    Serial.println("ID  = " + SigFox.ID());
    Serial.println("PAC = " + SigFox.PAC());
    Serial.println("SigFox Version = " + SigFox.SigVersion());
  }

  delay(100);

  SigFox.beginPacket();
  SigFox.write(value_to_send);
  int ret = SigFox.endPacket();

  if (DEBUG){
    Serial.print("Status : ");
    Serial.println(ret);
  }
}

void loop(){}
