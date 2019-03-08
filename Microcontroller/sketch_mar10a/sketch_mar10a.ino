#include <Encoder.h>


//   avoid using pins with LEDs attached

char buf[128];
void setup() {
  Serial.begin(9600);
  Serial.println("Basic Encoder Test:");
}


void loop() {
  Encoder myEnc1(18,26);
Encoder myEnc2(19,28);
Encoder myEnc3(20,30);
Encoder myEnc4(21,32);
  long newPosition1 = myEnc1.read();
   
  long newPosition2 = myEnc2.read();
   
  long newPosition3 = myEnc3.read();
   
  long newPosition4 = myEnc4.read();
    sprintf(buf, "NOSE :Left wheel: %d; Right: %d  TAIL :Left wheel: %d; Right: %d", (int)newPosition1, (int)newPosition2, (int)newPosition3, (int)newPosition4);
  Serial.println(buf);
   Serial.println(buf);
}
