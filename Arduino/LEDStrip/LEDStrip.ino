#include <FastLED.h>

#define dataPin 7
#define numLeds 39

String msg;

CRGB leds[numLeds];

//Command list: cmdType, index1, index2, r1, g1, b1
int cmd[6];
int s[3];
int delta[3];
int rgb[] = {0,0,0};

float dt;
float elapsed;
float pt = 0.0;
bool soundMode = false;

void cubicInterpolate(float dt);

void setup() {
  Serial.begin(9600);
  FastLED.addLeds<WS2812, dataPin, GRB>(leds, numLeds); 
  cmd[0] = -1;
}

void loop() {
   dt = millis()/1000.0 - pt;
   pt = millis()/1000.0;
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
    cmd[counter] = word.toInt();
    if(cmd[0] == 0){
      Serial.println("connected");
    }
    else if(cmd[0] == 1){
        delta[0] = cmd[3]-rgb[0];
        delta[1] = cmd[4]-rgb[1];
        delta[2] = cmd[5]-rgb[2];
        s[0] = rgb[0];
        s[1] = rgb[1];
        s[2] = rgb[2];
        elapsed = 0;
    } 
    else if(cmd[0] == 2){
        soundMode = true;
    }
    else if(cmd[0] == 3){
      soundMode = false;
    }
    Serial.flush();
  }
  if(!soundMode){
    cubicInterpolate(dt);
    for(int i = 0;i<numLeds;i++){
      leds[i] = CRGB(rgb[0], rgb[1], rgb[2]);
    }
    FastLED.show();
    delay(50);
  } else {
    soundResponseMode(cmd[1], cmd[2], cmd[3]);
  }
  
}

void cubicInterpolate(float dt){
  if(elapsed>5.0){
  elapsed = 5.0;
  }
  elapsed += dt;
  float factor = 1.0-pow(1.0-(abs(elapsed)/5.0),3);
  rgb[0] = (int)(s[0]+delta[0]*factor);
  rgb[1] = (int)(s[1]+delta[1]*factor);
  rgb[2] = (int)(s[2]+delta[2]*factor);   
  
}

void soundResponseMode(int r, int g, int b){
  int level = analogRead(A0);
  if(level >= 500){
    int num;
    if(level - 500 <= 117){
      num = ((level - 500) / 3);
    } else {
      num = 39;
    }
    for(int i = 0; i < num; i++){
      leds[i] = CRGB(r, g, b);
      FastLED.show();
      delay(10);
    }
    delay(10);
    for(int i = num-1; i >= 0; i--){
      leds[i] = CRGB(0, 0, 0);
      FastLED.show();
      delay(10);
    }
  } else {
    for(int i = 0; i < numLeds; i++){
      leds[i] = CRGB(0, 0, 0);
    }
    FastLED.show();
  }
}
