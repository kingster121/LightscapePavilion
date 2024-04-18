#include <FastLED.h>

const int LED_PIN = 22;
const int NUM_LEDS = 127;
const int LED_MAPPING[]= {17, 10, 11, 14, 11, 10};

const int NIGHT_PIN = 32;
const int DAY_PIN = 33;
const int PDLC[] = {21, 19, 18, 17, 16, 4};

CRGB leds[NUM_LEDS];

String onOffString;

void clearPDLC(){
  for (int i=0; i<6; i++){
    digitalWrite(PDLC[i], LOW);
  }
}

void dayTime(){
  FastLED.clear();
  for(int i=0; i<6; i++){
    if (onOffString[i] == '1') {
      digitalWrite(PDLC[i], HIGH);
    }
    else{
      digitalWrite(PDLC[i], LOW);
    }
  }
}

void nightTime(){
  clearPDLC();
  int startingLED = 0;
  for(int i=0; i<6; i++){
    if (onOffString[i] == '1'){
      for (int ledToOn = startingLED; ledToOn < (startingLED + LED_MAPPING[i]); ledToOn++){
        leds[ledToOn] = CRGB(255, 255, 255);
      }
    }
    else{
      for (int ledToOn = startingLED; ledToOn < (startingLED + LED_MAPPING[i]); ledToOn++){
        leds[ledToOn] = CRGB(0, 0, 0);
      }
    }
    startingLED += LED_MAPPING[i];
  }
}

void setup() { 
  Serial.begin(115200); 
  Serial.setTimeout(1);
  
  for (int i=0; i<6; i++){
    pinMode(PDLC[i], OUTPUT);
  }
  pinMode(NIGHT_PIN, INPUT);
  pinMode(DAY_PIN, INPUT);
  
  FastLED.addLeds<WS2812, LED_PIN, GRB>(leds, NUM_LEDS);
  FastLED.setBrightness(25);
} 

void loop() { 
//  FastLED.clear();
  
  while(!Serial.available());
  onOffString = Serial.readString();
  Serial.println(onOffString);

  int startingLED = 0;
//  Serial.print(digitalRead(isDay));
//  Serial.print(", ");
//  Serial.println(digitalRead(isNight));

//  bool isNight = digitalRead(NIGHT_PIN);
//  bool isDay = digitalRead(DAY_PIN);
//
//  Serial.print(isNight);
//  Serial.print(", ");
//  Serial.println(isDay);
//
//  if(isDay){
//    dayTime();
//  }
//  else if(isNight){
//    nightTime();
//  }
  
  for (int i=0; i<6; i++){
//     Processing the output based on input
    if (onOffString[i] == '1') {
      digitalWrite(PDLC[i], LOW ); 
      for (int ledToOn = startingLED; ledToOn < (startingLED + LED_MAPPING[i]); ledToOn++){
        leds[ledToOn] = CRGB(255, 255, 255);
      }
    }
    else if (onOffString[i] == '0'){
      digitalWrite(PDLC[i], HIGH);
      for (int ledToOn = startingLED; ledToOn < (startingLED + LED_MAPPING[i]); ledToOn++){
        leds[ledToOn] = CRGB(0, 0, 0);
      }
    }
    startingLED += LED_MAPPING[i];
  }

  FastLED.show();
  delay(1000);
} 
