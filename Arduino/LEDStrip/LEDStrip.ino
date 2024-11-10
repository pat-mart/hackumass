#include <FastLED.h>

#define dataPin 7
#define numLeds 39

CRGB leds[numLeds];

void setup() {
  FastLED.addLeds<WS2812, dataPin, GRB>(leds, numLeds); 
}

void loop() {
  for(int i = 0; i < numLeds; i++){
    leds[i] = CRGB(0, 0, 255);
    FastLED.show();
    delay(50);
    leds[i] = CRGB::Black;
  }
}
