#include <Servo.h>
#include <stdarg.h>
#include <Arduino.h>

// Mount the servos
Servo boltservo;

// Output channels from the Shopbot
int shopbot_OP09 = A0;
int shopbot_OP10 = A1;
int shopbot_OP11 = A2;
int shopbot_OP12 = A3;
float sb09 = 0;
float sb10 = 0; 
float sb11 = 0; 
float sb12 = 0;
bool BUSY=false;

// Stepper Motor Controllers
int dirbolt = 7;     // bolt direction (LOW = cclockwise(backwards))
int stumpbolt = 6;   // bolt step
int dirvox = 2;      // voxel direction
int stumpvox = 1;    // voxel step
int dirnut = 9;      // nut direction
int stumpnut = 8;    // nut step
int button = 3;      // dispense screw and nut
int buttonval;
int prevbuttonval;
int pos = 70;        // servo starting position
int screwsleep = 5;  //stepper motor low power mode

void setup() {
    // Set pin states
    pinMode(dirbolt, OUTPUT);
    pinMode(stumpbolt, OUTPUT);
    pinMode(dirvox, OUTPUT);
    pinMode(stumpvox, OUTPUT);
    pinMode(dirnut, OUTPUT);
    pinMode(stumpnut, OUTPUT);
    pinMode(button, INPUT);
    pinMode(screwsleep, OUTPUT);  
    digitalWrite(dirbolt, LOW);
    digitalWrite(dirvox, LOW);
    digitalWrite(dirnut, HIGH);
    digitalWrite(screwsleep, LOW);
    boltservo.attach(10);
    boltservo.write(70);

    Serial.begin(9600);

    Serial.println("Starting program...");
}


void loop() {
    // command from hw button press
    buttonval = digitalRead(3);
    if (buttonval == HIGH){
        load_rewindStack();
        prevbuttonval = buttonval;  // ? doesn't seem to be used
    }
    
    // command from shopbot
    sb09 = analogRead(shopbot_OP09);
    
    if (sb09 > 950 && BUSY==false) {       // if input pin 9 is high and shopbot is not busy
        BUSY=true;                         // shopbot is now busy
        // read the other input pins
        sb10 = analogRead(shopbot_OP10);
        sb11 = analogRead(shopbot_OP11);
        sb12 = analogRead(shopbot_OP12);
        
        if (sb10 < 950 && sb11 > 950 && sb12 < 950) {       // 10,11,12 = 0,1,0
            load_nextScrew();
        }
        else if (sb10 > 950 && sb11 < 950 && sb12 < 950) {  // 10,11,12 = 1,0,0
            load_nextVoxel();
        }
        else if (sb10 < 950 && sb11 < 950 && sb12 > 950) {  // 10,11,12 = 0,0,1
            load_nextNut(); 
        }
        else if (sb10 > 950 && sb11 > 950 && sb12 < 950) {  // 10,11,12 = 1,1,0
            load_bolt();
        }
        else{
            Serial.println("shopbot input signal not recognized")
        }
        BUSY=false;
        delay(500); // shopbot trigger pin 9 only stays hight for 0.5 seconds 
    }
    

    // command from serial keyboard entry   
    if (Serial.available() > 0){
        char c = Serial.read();
             
        switch (c) {
            case 's':
                load_nextScrew();
                break;
            case 'n':
                load_nextNut();
                break;
            case 'v':
                load_nextVoxel();
                break;
            case 'b':
                load_bolt();
                break;
            case 'r':
                load_rewindStack();
                break;
            default:
                Serial.println("keyboard serial input not recognized")
        }
    }

}


void load_nextScrew(){
    Serial.println("Next Screw");
    digitalWrite(screwsleep, HIGH);
    for (int i=0; i < 11; i++) {
        digitalWrite(dirbolt, LOW);
        digitalWrite(stumpbolt,HIGH); 
        delayMicroseconds(6000);
        digitalWrite(stumpbolt,LOW); 
        delayMicroseconds(6000);
    }
    digitalWrite(screwsleep, LOW);
}


void load_nextNut(){
    Serial.println("Next Nut");
    for (int i=0; i < 350; i++) {
        digitalWrite(dirnut, HIGH);
        digitalWrite(stumpnut,HIGH); 
        delayMicroseconds(6000);       
        digitalWrite(stumpnut,LOW); 
        delayMicroseconds(6000);
    }
}


void load_nextVoxel(){
    Serial.println("Next Voxel");
    for (int i=0; i < 50; i++) {
        digitalWrite(dirvox, LOW);
        digitalWrite(stumpvox,HIGH); 
        delayMicroseconds(6000);       
        digitalWrite(stumpvox,LOW); 
        delayMicroseconds(6000);
    }
}


void load_bolt(){
    Serial.println("Bolt Screw");
    for (pos = 70; pos <= 95; pos += 1) {  // goes from 0 degrees to 180 degrees, steps of 1 deg
        boltservo.write(pos);              // tell servo to go to position in variable 'pos'
        delay(30);                         // waits 15ms for the servo to reach the position
    }
    for (pos = 95; pos >= 70; pos -= 1) {  // goes from 180 degrees to 0 degrees
        boltservo.write(pos);              // tell servo to go to position in variable 'pos'
        delay(30);                         // waits 15ms for the servo to reach the position
    }
}


void load_rewindStack(){
    Serial.println("Rewind Stack");
    for (int i=0; i < 2100; i++) {
        digitalWrite(dirnut, LOW);        
        digitalWrite(stumpnut,HIGH); 
        delayMicroseconds(6000);       
        digitalWrite(stumpnut,LOW); 
        delayMicroseconds(6000);
    }
}


