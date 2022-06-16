//Libraries to Include
#include <Servo.h>

//Servo Initialization
Servo myservo;
Servo myservo2;

//Variable initialisation
String serialdata; //For incoming serial data
int midpoint = 90; //For setting the laser pointer to the middle of the frame

void setup() {
  myservo2.attach(1); //Y cordinate servo
  myservo.attach(2);  //X cordinate servo
  Serial.begin(115200); //Enabling Serial Communication
  Serial.setTimeout(10); //Setting a Serial Timeout

  //Initialize XY with 90 to set the midpoint
  myservo.write(midpoint);    //set X to 90
  myservo2.write(midpoint);   //Set Y to 90
}

void loop()
{
  //
}


int x,y=minpoint; //setting initial cordinates as middle of the frame

//this funtion is triggered while receving a serial data
void serialEvent()
{
  serialdata = Serial.readString();     //Reads incoming string serial data
  int cordinates = serialdata.toInt();  //converts incoming encoded string cordinates to integer for calculation

  //caluclating X-Y cordinates from the encoded string
  //cordinates will be in the form 2xxx0yyy eg:20390107
  //where xxx is the X cordinate and yyy will be Y cordinate eg:X=39 and Y=107
  y = cordinates%1000;          // to isolate the last 3 digits : Y cordinate eg: CCCCC107
  cordinates = cordinates-y;    // subtract the Y cordinate from the original string eg: 20390107 - 107 = 20390000
  x = (cordinates/10000)-2000;  // devide the cordinates by 100000 to get the first 4 digits and substract it from 2000 to get the x cordinate eg: 2039 - 2000 = 39 -> X cordinate

  myservo2.write(int(y)); //write y cordinate to the Y servo motor
  myservo.write(int(x));  //write x cordinate to the X servo motor
}
