# PROJETO FINAL CURSO CPS (PROGRAMAÇÃO PYTHON COM ARDUINO)
# DATALOGGER (TEMPERATURA, UMIDADE RELATIVA, PRESSÃO BAROMÉTRICA E ALTITUDE
# AUTOR: DANIEL RODRIGUES DE SOUSA 24/05/2023

import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
import tkinter as tk
import serial.tools.list_ports

# Inicializa Tkinter e Figura Matplotlib
root = tk.Tk()

# Título da janela
root.title('Dashboard para Arduino')

# Seta tela cheia para esta aplicação
largura = root.winfo_screenwidth()
altura = root.winfo_screenheight()
root.geometry('%dx%d' % (largura, altura))

# Força o fechamento do programa quando for clicado no icone 'x'
root.protocol('WM_DELETE_WINDOW', exit)

# Configura 'fig' para o canvas
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)

# Aplicação Tkinter (frame)
frame = tk.Frame(root)
label = tk.Label(text='Dashboard com Tkinter + Matplotlib!')
label.config(font=('Arial', 32))
label.pack()
frame.pack()

# Cria canvas
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Plota dados para a Figura Matplotlib
def animacao(i, listaGrafico1, listaGrafico2, listaGrafico3, listaGrafico4, ser):
    ser.write(b'a')  # Transmite o caractere 'a' para o Arduino
    arduinoDado_string1 = ser.readline().decode('ascii')  # Recebe o dado e decodifica a string

    ser.write(b'b')  # Transmite o caractere 'b' para o Arduino
    arduinoDado_string2 = ser.readline().decode('ascii')  # Recebe o dado e decodifica a string

    ser.write(b'c')  # Transmite o caractere 'c' para o Arduino
    arduinoDado_string3 = ser.readline().decode('ascii')  # Recebe o dado e decodifica a string

    ser.write(b'd')  # Transmite o caractere 'd' para o Arduino
    arduinoDado_string4 = ser.readline().decode('ascii')  # Recebe o dado e decodifica a string

    #print(i)                                           # 'i' é uma veriável baseada no argumento frames = x na função de animação

    try:
        arduinoDado_float1 = float(arduinoDado_string1)  # Converte para float
        arduinoDado_float2 = float(arduinoDado_string2)  # Converte para float
        arduinoDado_float3 = float(arduinoDado_string3)  # Converte para float
        arduinoDado_float4 = float(arduinoDado_string4)  # Converte para float

        listaGrafico1.append(arduinoDado_float1)  # Adiciona na lista o dado convertido para plotagem
        listaGrafico2.append(arduinoDado_float2)  # Adiciona na lista o dado convertido para plotagem
        listaGrafico3.append(arduinoDado_float3)  # Adiciona na lista o dado convertido para plotagem
        listaGrafico4.append(arduinoDado_float4)  # Adiciona na lista o dado convertido para plotagem

    except:
        pass

    listaGrafico1 = listaGrafico1[-50:]  # Ajusta a lista de valores com os últimos 50 dados recentes
    listaGrafico2 = listaGrafico2[-50:]  # Ajusta a lista de valores com os últimos 50 dados recentes
    listaGrafico3 = listaGrafico3[-50:]  # Ajusta a lista de valores com os últimos 50 dados recentes
    listaGrafico4 = listaGrafico4[-50:]  # Ajusta a lista de valores com os últimos 50 dados recentes

    min_valor1 = None   # inicializa dados com 'None' para captura dos valores máximos e mínimos
    max_valor1 = None

    min_valor2 = None
    max_valor2 = None

    min_valor3 = None
    max_valor3 = None

    min_valor4 = None
    max_valor4 = None

    for num in listaGrafico1:   # Verifica valor mínimo em listaGrafico1
        if (min_valor1 is None or num < min_valor1):
            min_valor1 = num

    for num in listaGrafico1:   # Verifica valor máximo em listaGrafico1
        if (max_valor1 is None or num > max_valor1):
            max_valor1 = num

    for num in listaGrafico2:   # Verifica valor mínimo em listaGrafico2
        if (min_valor2 is None or num < min_valor2):
            min_valor2 = num

    for num in listaGrafico2:   # Verifica valor máximo em listaGrafico2
        if (max_valor2 is None or num > max_valor2):
            max_valor2 = num

    for num in listaGrafico3:   # Verifica valor mínimo em listaGrafico3
        if (min_valor3 is None or num < min_valor3):
            min_valor3 = num

    for num in listaGrafico3:   # Verifica valor máximo em listaGrafico3
        if (max_valor3 is None or num > max_valor3):
            max_valor3 = num

    for num in listaGrafico4:   # Verifica valor mínimo em listaGrafico4
        if (min_valor4 is None or num < min_valor4):
            min_valor4 = num

    for num in listaGrafico4:   # Verifica valor máximo em listaGrafico4
        if (max_valor4 is None or num > max_valor4):
            max_valor4 = num

    ax1.clear()  # Limpa último frame com os dados
    ax1.plot(listaGrafico1)  # Plota novo frame
    ax1.set_ylim([min_valor1-0.01, max_valor1+0.01])  # Seta os limites do eixo vertical
    ax1.set_title('Temperatura (C)')  # Seta o título do gráfico
    ax1.set_ylabel('Valor')  # Seta o título do eixo vertical

    ax2.clear()  # Limpa último frame com os dados
    ax2.plot(listaGrafico2)  # Plota novo frame
    ax2.set_ylim([min_valor2-0.01, max_valor2+0.01])  # Seta os limites do eixo vertical
    ax2.set_title('Umidade (%)')  # Seta o título do gráfico
    ax2.set_ylabel('Valor')  # Seta o título do eixo vertical

    ax3.clear()  # Limpa último frame com os dados
    ax3.plot(listaGrafico3)  # Plota novo frame
    ax3.set_ylim([min_valor3-10, max_valor3+10])  # Seta os limites do eixo vertical
    ax3.set_title('Pressão (Pa)')  # Seta o título do gráfico
    ax3.set_ylabel('Valor')  # Seta o título do eixo vertical

    ax4.clear()  # Limpa último frame com os dados
    ax4.plot(listaGrafico4)  # Plota novo frame
    ax4.set_ylim([min_valor4-0.1, max_valor4+0.1])  # Seta os limites do eixo vertical
    ax4.set_title('Altitude (m)')  # Seta o título do gráfico
    ax4.set_ylabel('Valor')  # Seta o título do eixo vertical

listaGrafico1 = []  # Cria lista vazia para uso
listaGrafico2 = []  # Cria lista vazia para uso
listaGrafico3 = []  # Cria lista vazia para uso
listaGrafico4 = []  # Cria lista vazia para uso

# Detecção automática de COM atrelada ao Arduino

flag_port_ok = 0    # Seta um flag para detecção
for port in serial.tools.list_ports.comports():         # Laço onde a cada interação é testado as COMs instaladas
    ser = serial.Serial(port.name, 115200, timeout=1)   # Abre a COM com um timeout de leitura de 1 segundo
    time.sleep(2)                                   # Aguarda 2 segundos
    ser.write(b'$')                                 # Transmite o caractere '$'
    if ser.readline().decode('ascii') == 'ok\r\n':  # Lê o dado e checa se recebeu 'ok\r\n'
        flag_port_ok = 1    # Se sim, seta o flag de detecção
        break               # Força a saída do laço

if flag_port_ok == 0:       # Se porta não detectada ou a COM não o tem Arduino, fecha o programa
    exit()

ser.flushInput()            # Caso contrário, limpa buffer de entrada e saída
ser.flushOutput()
ser.close()                 # Fecha a serial

ser = serial.Serial(port.name, 115200)  # Reabre a COM sem timeout de leitura
time.sleep(2)  # Aguarda 2 segundos

# Inicialização do gráfico:

# fig -> 'figura' a ser tratado pelo canvas
# animacao -> chamada da função com a animação (gráficos)
# frames -> número de frames por segundo (primeiro argumento utilizado na função 'animacao')
# fargs -> tupla com o restante dos argumentos da função 'animacao'
# interval -> tempo de atualização entre imagens

ani = animation.FuncAnimation(fig, animacao, frames=100, fargs=(listaGrafico1, listaGrafico2, listaGrafico3, listaGrafico4, ser), interval=250)

canvas.draw()   # chama o canvas e desenha o que está em fig
root.mainloop() # loop da janela