/* Эта программа основаня на программе тестирования энкодеров. Здесь же проводится расчет
    скоростей вращения колес. Каждые ~ 20 миллисекунд вызываются функции рассчета скоростей
    для каждого колеса. Сами функции рассчета скоростей оперируют значениями тиков, которые
    все время рассчитываются в прерываниях независимо от главного цикла.
*/
#include <PinChangeInt.h>

//считывающие пины для энкодеров
#define NLENCY 44  //N - nose, L - left, Y -yellow
#define NLENCG 43  //G - green
#define NRENCY 33  //R - right
#define NRENCG 42
#define TLENCY 48  //T - tail
#define TLENCG 52
#define TRENCY 53
#define TRENCG 47

// pwm pins 2 - right up 4 - left up  6 - right down 8 - left down
#define NLCW 3 
#define NLCCW 4
#define TLCW 3
#define TLCCW

// digital pins 22 - right up 23 - left up 24 - right down  25 - left down
#define RCCW 8
#define RCW 7
#define RCCW 8
#define RCW 


int req_vel = 280; //Put into the ROS
int error, analogchange;
int lerrorold = 0;
int rerrorold = 0;
float p = 0.35;
float i = 0.5;
float d = 0.002;
float deriv;
float lerrint = 0;
float rerrint = 0;

char buf[128];
int ltickes, rtickes, ltickeslast, rtickeslast;
int FL_vel, FR_vel, BL_vel, BR_vel; //скорости правого и левого колес
long timer; //таймер, тип long (больше, чем int, но тоже число будет кончено)
int delta;  //дельта времени замера

void setup() {
  Serial.begin(9600);

  pinMode( FLENCA, INPUT);
  pinMode( FLENCB, INPUT);
  pinMode( FRENCA, INPUT);
  pinMode( FRENCB, INPUT);
  pinMode( BLENCA, INPUT);
  pinMode( BLENCB, INPUT);
  pinMode( BRENCA, INPUT);
  pinMode( BRENCB, INPUT);

  pinMode(LCW, OUTPUT);
  pinMode(LCCW, OUTPUT);
  pinMode(LEN, OUTPUT);
  pinMode(LPWM, OUTPUT);

  pinMode(RCW, OUTPUT);
  pinMode(RCCW, OUTPUT);
  pinMode(REN, OUTPUT);
  pinMode(RPWM, OUTPUT);


  Serial.println("---------------------------------------");
  attachPinChangeInterrupt(LENCA, LinterruptFunc, FALLING);
  attachPinChangeInterrupt(RENCA, RinterruptFunc, FALLING);
  ltickes = 0;
  rtickes = 0;
  timer = millis(); //начальный момент времени
}

void loop() {
  //замеряем дельту времени каждую итерацию цикла. Если она будет >= 20 миллисекунд, то
  if ((delta = millis() - timer) >= 20)
  {
    //рассчитываем скорость левого колеса
    Lvelcalc();
    //ошибка левого колеса
    error = (-reqvel) - Lvel;
    //рассчет интеграла
    lerrint += error * delta / 1000;
    //рассчет дифференциальной составляющей
    deriv = (error- lerrorold) / (delta / 1000);
    lerrorold = error;
    //рассчет компинсации
    analogchange = error * p + lerrint * i + deriv * d;
    //сама компинсация
    Lmove(analogchange);
    //аналогично для правого
    Rvelcalc();
    error = reqvel - Rvel;
    rerrint += error * ((float)delta / 1000);
    deriv = (error- rerrorold) / ((float)delta / 1000);
    rerrorold = error;
    analogchange = error * p + rerrint * i + deriv * d;
    Rmove(analogchange);

    timer = millis();
  }
  sprintf(buf, "Left wheel: %d; Right: %d", (int)Lvel, (int)Rvel);
  Serial.println(buf);
    Serial.println(deriv * d);
}

//Функции расчета скоростей
void Lvelcalc() {
  /*Скорость равна количеству оборотов за единицу времени * длину дуги колеса.
    Длина дуги колеса = PI * D, где D = 82 мм.
    Количество оборотов за единицу времени = разность тиков, деленная на количество тиков за оборот
    и умноженная на дельту времени (так как дельта времени в миллисекундах, то ее делим на 1000).
    Количество тиков за ~ равно 390.1 (определяется документацией на энкодер).
  */
  Lvel = ((ltickes / 390.1) * 1000 / delta) * PI * 82;
  ltickes = 0; //обнуляем тики, чтобы не допустить переполнение переменной тиков
}

void Rvelcalc() {
  Rvel = ((rtickes / 390.1) * 1000 / delta) * PI * 82;
  rtickes = 0;
}

//Функции расчета тиков
void LinterruptFunc() {
  if (digitalRead(LENCB))
    ltickes++;
  else
    ltickes--;
}

void RinterruptFunc() {
  if (digitalRead(RENCB))
    rtickes++;
  else
    rtickes--;
}

//функции движения колес

void Lmove( int speed)
{
  // если скорость больше или равна 0, то вращаем по часовой стрелки
  if (speed >= 0)
  {
    digitalWrite(LCW, HIGH); //Выставляем пин "По часовой стрелке" в 1
    digitalWrite(LCCW, LOW); //А против часовой- в 0.
  }
  else //если меньше- против часовой
  {
    speed = -speed; //Помним, что analogWrite воспринимает только положительные значения
    digitalWrite(LCCW, HIGH); //аналогично
    digitalWrite(LCW, LOW);
  }

  analogWrite(LPWM, speed); //И теперь уже выставляем саму скорость.
}

void Rmove( int speed)
{
  if (speed >= 0)
  {
    digitalWrite(RCW, HIGH);
    digitalWrite(RCCW, LOW);
  }
  else
  {
    speed = -speed;
    digitalWrite(RCCW, HIGH);
    digitalWrite(RCW, LOW);
  }

  analogWrite(RPWM, speed);
}
