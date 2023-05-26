/* PROJETO FINAL CURSO CPS (PROGRAMAÇÃO PYTHON COM ARDUINO)
 * DATALOGGER (TEMPERATURA, UMIDADE RELATIVA, PRESSÃO BAROMÉTRICA E ALTITUDE
 * 
 * ARDUINO UNO
 * LCD OLED SSD1306
 * SENSOR DE UMIDADE RELATIVA E TEMPERATURA SHT31
 * SENSOR DE PRESSÃO BAROMÉTRICA E TEMPERATURA BMP085
 * PROTOSHIELD ARDUINO
 * 
 * AUTOR: DANIEL RODRIGUES DE SOUSA 24/05/2023 */

//INCLUSÃO DAS BIBLIOTECAS NECESSÁRIAS
#include <Arduino.h>
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_SHT31.h>
#include <Adafruit_BMP085.h>

//CONFIGURAÇÃO DO DISPLAY OLED
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

#define OLED_RESET     -1
#define SCREEN_ADDRESS 0x3C

//CONSTANTE DE TEMPO USADO NO PROGRAMA
#define TEMPO_MS  166

//DEFINIÇÃO DAS VARIÁVEIS UTILIZADAS PARA ACESSO AOS MÓDULOS
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);
Adafruit_SHT31 sht31 = Adafruit_SHT31();
Adafruit_BMP085 bmp;

//VARIÁVEIS DE USO GERAL
char comando;
char state = 0;
long tempo;
long tempo_ant;

//VARIÁVEIS DE USO DOS MÓDULOS
float temp1, temp2;
float umidade;
long int pressao;
float altitude;

//FUNÇÃO PARA ATUALIZAÇÃO DOS DADOS NO DISPLAY OLED
void atualiza_display(void)
{
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  
  display.setCursor(0,0);
  display.print("Temp. (C) = ");
  display.print((temp1 + temp2)/2); 
  
  display.setCursor(0,10);
  display.print("Umid. (%) = ");
  display.print(umidade); 
  
  display.setCursor(0,20);
  display.print("Pres.(Pa) = ");
  display.print(pressao);
  
  display.setCursor(0,30);
  display.print("Altitude (m) = ");
  display.print(altitude);
  
  display.display(); 
}

void setup()
{
  //CONFIGURAÇÕES INICIAIS: SERIAL E MÓDULOS
  Serial.begin(115200);
  
  if(!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS))
  {
    Serial.println("Erro display!");
    while(1);
  }
  
  if(!sht31.begin(0x44))
  {
    Serial.println("Erro SHT31!");
    while(1);
  }

  if(!bmp.begin()) 
  {
    Serial.println("Erro BMP085!");  
    while(1);
  }
}

void loop()
{
  int i;  //VARIÁVEL DE USO GERAL
      
  if(Serial.available() > 0)  //TEM DADO DISPONÍVEL?
  {
    comando = Serial.read();  //LEITURA DO CARACTERE (COMANDO)
    
    switch(comando)
    {
      case '$':                 //SE COMANDO '$', ENVIA 'ok' PARA
        for(i=0; i<100; i++)    //RECONHECIMENTO DE PORTA SERIAL
        {                       //(ENVIA 100 VEZES PARA GARANTIR
          Serial.println("ok"); //RECEBIMENTO NO APLICATIVO
          delay(10);
        }
        break;
        
      case 'a':                 //SE COMANDO 'a', ENVIA TEMPERATURA
        Serial.println((temp1 + temp2)/2);
        break;

      case 'b':                 //SE COMANDO 'b', ENVIA UMIDADE
        Serial.println(umidade);
        break;

      case 'c':                 //SE COMANDO 'c', ENVIA PRESSÃO BAROMÉTRICA
        Serial.println(pressao);
        break;

      case 'd':                 //SE COMANDO 'd', ENVIA ALTITUDE
        Serial.println(altitude);
        break;
    }
  }

  tempo = millis();

  if(tempo - tempo_ant >= TEMPO_MS) //TMPORIZAÇÃO A CADA 166 ms
  {                                 //(UM CICLO COMPLETO A CADA SEGUNDO)
    tempo_ant = tempo;

    switch(state)
    {
      case 0:                           //ESTADO '0' -> LÊ TEMPERATURA
        temp1 = sht31.readTemperature();//DO SENSOR STH31
        state++;
        break;

      case 1:                           //ESTADO '1' -> LÊ UMIDADE
        umidade = sht31.readHumidity(); //DO SENSOR STH31
        state++;
        break;

      case 2:                           //ESTADO '2' -> LÊ TEMPERATURA
        temp2 = bmp.readTemperature();  //DO SENSOR BMP085
        state++;
        break;

      case 3:                           //ESTADO '3' -> LÊ PRESSÃO
        pressao = bmp.readPressure();   //DO SENSOR BMP085
        state++;
        break;

      case 4:                           //ESTADO '4' -> LÊ ALTITUDE
        altitude = bmp.readAltitude();  //DO SENSOR BMP085
        state++;
        break;

      case 5:                           //ESTADO '5' -> ATUALIZA DISPLAY
        atualiza_display();
        state=0;
        break;
    }
  }
}
