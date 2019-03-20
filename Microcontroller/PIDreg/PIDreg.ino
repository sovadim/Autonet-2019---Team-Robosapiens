<<<<<<< HEAD
#include <Encoder.h>

=======
>>>>>>> fd8439e0f376de4dae51afea5e9e03671d78705b
/* Эта программа основаня на программе тестирования энкодеров. Здесь же проводится расчет
    скоростей вращения колес. Каждые ~ 20 миллисекунд вызываются функции рассчета скоростей
    для каждого колеса. Сами функции рассчета скоростей оперируют значениями тиков, которые
    все время рассчитываются в прерываниях независимо от главного цикла.
*/
#include <PinChangeInt.h>
<<<<<<< HEAD
//считывающие пины для энкодеров
#define NRENCY 19  //N - nose, L - left, Y -yellow
#define NRENCG 28  //G - green
#define NLENCY 18  //R - right
#define NLENCG 26
//#define TLENCY 20  //T - tail
//#define TLENCG 30
//#define TRENCY 21
//#define TRENCG 32
Encoder encNL(NLENCY,NLENCG);
Encoder encNR(NRENCY,NRENCG);
#define NLCW 6 
#define NLCCW 7
#define NRCW 2
#define NRCCW 3


#define TLCCW 11
#define TLCW 12
#define TRCCW 10
#define TRCW 9


#define PNL 0.45
#define INL 0
#define DNL 0
#define PNR 0
#define INR 0
#define DNR 0
#define PTL 0
#define ITL 0
#define DTL 0
#define PTR 0
#define ITR 0
#define DTR 0
#define DIAMETER 67
#define TICKVALUE 1


int reqvel = 256;  //Put into the ROS
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
void NLvelcalc();
void NRvelcalc();
void TLvelcalc();
void TRvelcalc();
void NLGinterruptFunc();
void NRGinterruptFunc();
void TLGinterruptFunc();
void TRGinterruptFunc();
void NLmove( int speed);
void NRmove( int speed);
void TLmove( int speed);
void TRmove( int speed);


>>>>>>> fd8439e0f376de4dae51afea5e9e03671d78705b

void setup() {
  Serial.begin(9600);

<<<<<<< HEAD
  pinMode(NLENCY, INPUT);
  pinMode(NLENCG, INPUT);
  pinMode(NRENCY, INPUT);
  pinMode(NRENCG, INPUT);
//  pinMode(TLENCY, INPUT);
//  pinMode(TLENCG, INPUT);
//  pinMode(TRENCY, INPUT);
//  pinMode(TRENCG, INPUT);

 
  pinMode(NLCW, OUTPUT);
  pinMode(NLCCW, OUTPUT);
  pinMode(NRCW, OUTPUT);
  pinMode(NRCCW, OUTPUT);

  pinMode(TLCW, OUTPUT);
  pinMode(TLCCW, OUTPUT);
  pinMode(TRCW, OUTPUT);
  pinMode(TRCCW, OUTPUT);



  Serial.println("---------------------------------------");
//  attachInterrupt(digitalPinToInterrupt(NLENCG), NLGinterruptFunc, FALLING);
  attachInterrupt(NLENCY, NLYinterruptFunc, FALLING);
//  attachInterrupt(digitalPinToInterrupt(NRENCY), NRYinterruptFunc, FALLING);
  attachInterrupt(NRENCG, NRGinterruptFunc, FALLING);
//  attachInterrupt(digitalPinToInterrupt(TLENCY), TLYinterruptFunc, FALLING);
//  attachInterrupt(digitalPinToInterrupt(TLENCG), TLGinterruptFunc, FALLING);
//  attachInterrupt(digitalPinToInterrupt(TRENCY), TLYinterruptFunc, FALLING);
//  attachInterrupt(digitalPinToInterrupt(TRENCG), TLGinterruptFunc, FALLING);
  
  nltickes = 0;
  nrtickes = 0;
  tltickes = 0;
  trtickes = 0;

>>>>>>> fd8439e0f376de4dae51afea5e9e03671d78705b
  timer = millis(); //начальный момент времени
}

void loop() {
<<<<<<< HEAD
  

  //замеряем дельту времени каждую итерацию цикла. Если она будет >= 20 миллисекунд, то
  if ((delta = millis() - timer) >= 30)
  {
//-------------------------------функции задания скоростей
//-----------------------------------------------------------------------------NL
    NLvelcalc();
    error = reqvel - NLvel;  //ошибка левого колеса
    nlerrint += error * delta / 1000;  //рассчет интеграла
    deriv = (error- nlerrorold) / (delta / 1000);  //рассчет дифференциальной составляюще
    nlerrorold = error;
    analogchange = error * PNL + nlerrint * INL + deriv * DNL;  //рассчет компенсации 
    NLmove(analogchange);  //сама компенсация
//-----------------------------------------------------------------------------NR
    NRvelcalc();
    error = reqvel - NRvel;
    nrerrint += error * ((float)delta / 1000);
    deriv = (error- nrerrorold) / ((float)delta / 1000);
    nrerrorold = error;
    analogchange = error * PNR + nrerrint * INR + deriv * DNR;
    NRmove(analogchange);
//-----------------------------------------------------------------------------TL
    TLvelcalc();
    error = reqvel - TLvel;  //fixing motors
    tlerrint += error * ((float)delta / 1000);
    deriv = (error- tlerrorold) / ((float)delta / 1000);
    tlerrorold = error;
    analogchange = error * PTL + tlerrint * ITL + deriv * DTL;
    TLmove(analogchange);
//-----------------------------------------------------------------------------TR
    TRvelcalc();
    error = reqvel - TRvel;  //fixing motors
    trerrint += error * ((float)delta / 1000);
    deriv = (error- trerrorold) / ((float)delta / 1000);
    trerrorold = error;
    analogchange = error * PTR + trerrint * ITR + deriv * DTR;
    TRmove(analogchange);
    timer = millis();
  }
  sprintf(buf, "NOSE :Left wheel: %d; Right: %d  TAIL :Left wheel: %d; Right: %d", (int)NLvel, (int)NRvel, (int)TLvel, (int)TRvel);
  Serial.println(buf);
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
//  nltickes = encNL.read();
  NLvel = ((nltickes / TICKVALUE) * 1000 / delta) * PI * DIAMETER;
//  Encoder encNL(NLENCY,NLENCG);
  nltickes = 0;
}
//-----------------------------------------------------------------------------NR
void NRvelcalc() {
//  nrtickes = encNR.read();
  NRvel = ((nrtickes / TICKVALUE) * 1000 / delta) * PI * DIAMETER;
//  Encoder encNR(NRENCY,NRENCG);
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
//-----------------------------------------------------------------------------NLG
//void NLGinterruptFunc() {
//    nltickes++;
//}
////-----------------------------------------------------------------------------NLY
void NLYinterruptFunc() {
    nltickes++;
}
////-----------------------------------------------------------------------------NRG
void NRGinterruptFunc() {
    nrtickes++;
}
////-----------------------------------------------------------------------------NRY
//
////-----------------------------------------------------------------------------TLG
//void TLGinterruptFunc() {
//    tltickes++;
//}
////-----------------------------------------------------------------------------TLY
//
////-----------------------------------------------------------------------------TRG
//void TRGinterruptFunc() {
//    trtickes++;
//}
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
    analogWrite(NLCCW, speed);
    digitalWrite(NLCW, LOW);
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
    analogWrite(NRCCW, speed);
    digitalWrite(NRCW, LOW);
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
    analogWrite(TLCCW, speed);
    digitalWrite(TLCW, LOW);
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
    analogWrite(TRCCW, speed);
    digitalWrite(TRCW, LOW);
  }
}
