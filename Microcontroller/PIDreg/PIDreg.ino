
#include <Encoder.h>
#include <Servo.h>

/* Эта программа основаня на программе тестирования энкодеров. Здесь же проводится расчет
    скоростей вращения колес. Каждые ~ 20 миллисекунд вызываются функции рассчета скоростей
    для каждого колеса. Сами функции рассчета скоростей оперируют значениями тиков, которые
    все время рассчитываются в прерываниях независимо от главного цикла.
*/
#include <PinChangeInt.h>
//считывающие пины для энкодеров
#define NRENC 19  //N - nose, L - left, Y -yellow  //G - green
#define NLENC 18  //R - right  //T - tail
#define TLENC 21
#define TRENC 20

#define CATH_PIN 46

#define NLCW 7 
#define NLCCW 6
#define NRCW 3
#define NRCCW 2


#define TLCCW 12
#define TLCW 11
#define TRCCW 9
#define TRCW 10


#define PNL 0.3
#define INL 0.3
#define PNR 0.3
#define INR 0.3
#define PTL 0.3
#define ITL 0.3
#define PTR 0.3
#define ITR 0.3
#define DIAMETER 67
#define TICKVALUE 390.1

Servo servo1;


int reqvel = 500;  //Put into the ROS
int error, analogchange;
int nlerrorold = 0;
int nrerrorold = 0;
int tlerrorold = 0;
int trerrorold = 0;
float deriv;
float nlerrint = 0;
float nrerrint = 0;
float tlerrint = 0;
float trerrint = 0;

char buf[128];
int nltickes, nrtickes, tltickes, trtickes;
int NLvel, NRvel, TLvel, TRvel;  //скорости колес
long timer;
int delta;  //дельта времени замера


void setup() {
  Serial.begin(9600);
  pinMode(NLENC, INPUT);
  pinMode(NRENC, INPUT);
  pinMode(TLENC, INPUT);
  pinMode(TRENC, INPUT);
 
  pinMode(NLCW, OUTPUT);
  pinMode(NLCCW, OUTPUT);
  pinMode(NRCW, OUTPUT);
  pinMode(NRCCW, OUTPUT);
  servo1.attach(CATH_PIN);

   Serial.println("---------------------------------------");
  attachInterrupt(digitalPinToInterrupt(NLENC), NLinterruptFunc, FALLING);
  attachInterrupt(digitalPinToInterrupt(NRENC), NRinterruptFunc, FALLING);
  attachInterrupt(digitalPinToInterrupt(TLENC), TLinterruptFunc, FALLING);
  attachInterrupt(digitalPinToInterrupt(TRENC), TRinterruptFunc, FALLING);
  
  nltickes = 0;
  nrtickes = 0;
  tltickes = 0;
  trtickes = 0;

  timer = millis(); //начальный момент времени
}

void loop() {

  

  //замеряем дельту времени каждую итерацию цикла. Если она будет >= 20 миллисекунд, то
  if ((delta = millis() - timer) >= 20)
  {
//-------------------------------функции задания скоростей
//-----------------------------------------------------------------------------NL
    NLvelcalc();
    error = reqvel - NLvel;  //ошибка левого колеса
    nlerrint += error * delta / 1000;  //рассчет интеграла
    analogchange = error * PNL + nlerrint * INL;  //рассчет компенсации 
    NLmove(analogchange);  //сама компенсация
//-----------------------------------------------------------------------------NR
    NRvelcalc();
    error = reqvel - NRvel;
    nrerrint += error * ((float)delta / 1000);
    analogchange = error * PNR + nrerrint * INR ;
    NRmove(analogchange);
//-----------------------------------------------------------------------------TL
    TLvelcalc();
    error = reqvel - TLvel;  //fixing motors
    tlerrint += error * ((float)delta / 1000);
    analogchange = error * PTL + tlerrint * ITL ;
    TLmove(analogchange);
//-----------------------------------------------------------------------------TR
    TRvelcalc();
    error = reqvel - TRvel;  //fixing motors
    trerrint += error * ((float)delta / 1000);
    //if (trerrint >500 ) trerrint = 500;
    analogchange = error * PTR + trerrint * ITR ;
    TRmove(analogchange);
    timer = millis();
  }
  sprintf(buf, "NOSE :Left wheel: %d; Right: %d  TAIL :Left wheel: %d; Right: %d", (int)NLvel, (int)NRvel, (int)TLvel, (int)TRvel);
  Serial.println(buf);
  servo1.write(119);
  //sprintf(buf, "NOSE :Left wheel: %d; Right: %d  TAIL :Left wheel: %d; Right: %d", (int)(deriv * DNL), (int)(deriv * DNR), (int)(deriv * DTL), (int)(deriv * DTR));
  //Serial.println(buf);
}

//---------------------------------Функции расчета реальных скоростей
  /*Скорость равна количеству оборотов за единицу времени * длину дуги колеса.
    Длина дуги колеса = PI * D, где D = 67 мм.
    Количество оборотов за единицу времени = разность тиков, деленная на количество тиков за оборот
    и умноженная на дельту времени (так как дельта времени в миллисекундах, то ее делим на 1000).
  */
//-----------------------------------------------------------------------------NL
void NLvelcalc() {
  NLvel = ((nltickes / TICKVALUE) * 1000 / delta) * PI * DIAMETER;
  nltickes = 0;
}
//-----------------------------------------------------------------------------NR
void NRvelcalc() {
  NRvel = ((nrtickes / TICKVALUE) * 1000 / delta) * PI * DIAMETER;
  nrtickes = 0;
}
//-----------------------------------------------------------------------------TL
void TLvelcalc() {
  TLvel = ((tltickes / TICKVALUE) * 1000 / delta) * PI * DIAMETER;
  tltickes = 0;
}
//-----------------------------------------------------------------------------TR
void TRvelcalc() {
  TRvel = ((trtickes / TICKVALUE) * 1000 / delta) * PI * DIAMETER;
  trtickes = 0;
}
//-------------------------------------Функции расчета тиков
//-----------------------------------------------------------------------------NL
////-----------------------------------------------------------------------------NLY
void NLinterruptFunc() {
    nltickes++;
}
////-----------------------------------------------------------------------------NRG
void NRinterruptFunc() {
    nrtickes++;
}
////-----------------------------------------------------------------------------NRY
//
////-----------------------------------------------------------------------------TLG
void TLinterruptFunc() {
    tltickes++;
}
////-----------------------------------------------------------------------------TLY
//
////-----------------------------------------------------------------------------TRG
void TRinterruptFunc() {
    trtickes++;
}
//-----------------------------------------------------------------------------TRY


//---------------------------------функции движения колес
//-----------------------------------------------------------------------------NL
void NLmove( int speed)
{
  if (speed >= 0)
  {
    analogWrite(NLCW, speed);
    digitalWrite(NLCCW, LOW);
  }
  else
  {
    speed = -speed;
    analogWrite(NLCW, speed);
    digitalWrite(NLCCW, LOW);
  }
}
//-----------------------------------------------------------------------------NR
void NRmove( int speed)
{
  if (speed >= 0)
  {
    analogWrite(NRCW, speed);
    digitalWrite(NRCCW, LOW);
  }
  else
  {
    speed = -speed;
    analogWrite(NRCW, speed);
    digitalWrite(NRCCW, LOW);
  }
}
//-----------------------------------------------------------------------------TL
void TLmove( int speed)
{
  if (speed >= 0)
  {
    analogWrite(TLCW, speed);
    digitalWrite(TLCCW, LOW);
  }
  else 
  {
    speed = -speed;
    analogWrite(TLCW, speed);
    digitalWrite(TLCCW, LOW);
  }
}
//-----------------------------------------------------------------------------TR
void TRmove( int speed)
{
  if (speed >= 0)
  {
    analogWrite(TRCW, speed);
    digitalWrite(TRCCW, LOW);
  }
  else
  {
    speed = -speed; 
    analogWrite(TRCW, speed);
    digitalWrite(TRCCW, LOW);
  }
}
