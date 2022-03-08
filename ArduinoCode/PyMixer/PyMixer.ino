int reg = 0, flag = 0, ino = 0;
#define BTN 5

#define PIN_POT     A0
void setup(){

  Serial.begin(115200);
  pinMode(PIN_POT, INPUT);
  pinMode(BTN,INPUT_PULLUP);
  pinMode(13, OUTPUT);

  pinMode(12, OUTPUT);
  pinMode(16, OUTPUT);
  pinMode(4, OUTPUT);
}


void loop() {

   if(digitalRead(BTN) == HIGH &&flag==0)//если кнопка нажата   
     // и перемення flag равна 0 , то ... 
     { 
       reg++;   
       flag=1; 
         
        //это нужно для того что бы с каждым нажатием кнопки 
        //происходило только одно действие 
        // плюс защита от "дребезга"  100% 
          
        if(reg>4)//ограничим количество режимов 
        { 
          reg=1;//так как мы используем только одну кнопку, 
                    // то переключать режимы будем циклично 
        } 
       
     } 
       
      if(digitalRead(BTN) == LOW &&flag==1)
      //если кнопка НЕ нажата yyy
     //и переменная flag равна - 1 ,то ... 
     { 
          
        flag=0;//обнуляем переменную "knopka" 
     } 
      
       
       
    if(reg==1)//первый режим 
    { 
      digitalWrite(13, LOW);
digitalWrite(16, HIGH);
digitalWrite(12, HIGH);
digitalWrite(4, HIGH);
fio();
        
        
      //здесь может быть любое ваше действие 
    } 
    if(reg==2)//второй режим 
    { 
      digitalWrite(12, LOW);
digitalWrite(13, HIGH);
digitalWrite(4, HIGH);
digitalWrite(16, HIGH);
fio();
        
      //здесь может быть любое ваше действие 
    } 
      
    if(reg==3)//третий режим 
    { 
      digitalWrite(4, LOW);
digitalWrite(13, HIGH);
digitalWrite(12, HIGH);
digitalWrite(16, HIGH);
fio();

        
      //здесь может быть любое ваше действие 
    } 
      
    if(reg==4)//четвертый режим 
    { 
      digitalWrite(16, LOW);
digitalWrite(12, HIGH);
digitalWrite(13, HIGH);
digitalWrite(4, HIGH);
fio();

      //здесь может быть любое ваше действие 
    } 
      
 }

}

void fio(){
  if (analogRead(PIN_POT) != ino){
  ino = analogRead(PIN_POT)/10.24;
  Serial.print(reg);
 Serial.print(',');
   if (ino == 1){
    ino = 0;
    Serial.print(ino);
    Serial.print('\n');
    delay(10);}
    else {
   Serial.print(ino);
   Serial.print('\n');
   delay(10);
      }}
  }
