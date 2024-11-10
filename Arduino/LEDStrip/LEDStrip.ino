#include <FastLED.h>

#define dataPin 7
#define numLeds 39

String msg;

CRGB leds[numLeds];

//Command list: cmdType, index1, index2, r1, g1, b1
int cmd[6];
void setup() {
  Serial.begin(9600);
  FastLED.addLeds<WS2812, dataPin, GRB>(leds, numLeds); 
  cmd[0] = -1;
}

void loop() {
  if(Serial.available() > 0){
    msg = Serial.readStringUntil('\n');
    String word = "";
    int counter = 0;
    for(int i = 0; i < msg.length(); i++){
      if(msg[i] != ' '){
        word += msg[i];
      } else {
        cmd[counter] = word.toInt();
        word = "";
        counter++;
      }  
    }
    if(cmd[0] == 0){
      Serial.println("connected");
    }
    else if(cmd[0] == 1){
      for(int i = cmd[1]; i < cmd[2]; i++){
        leds[i] = CRGB(cmd[3], cmd[4], cmd[5]);
      }
    }
    Serial.flush();
  }

    
  FastLED.show();
  delay(50);
  
}
