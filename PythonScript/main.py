#pyinstaller --icon=app.ico --noconsole main.py
from __future__ import print_function
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
from PyQt5 import QtWidgets, uic #интерфейс
from PyQt5.QtWidgets import QComboBox  #интерфейс
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo #serial port
from PyQt5.QtCore import QIODevice
from PyQt5.QtGui import QIcon #библиотека для иконки
from Paradoxis import Sound #библиотека для звука
from Paradoxis import Keyboard #библиотека для звука
import subprocess

app = QtWidgets.QApplication([])
ui = uic.loadUi("main.sk") # загружаем интерфейс
ui.setWindowTitle("PyMixer") # устанавливам название файла
ui.setWindowIcon(QIcon('icon.png')) # устанавливам иконку файла
serial = QSerialPort()
serial.setBaudRate(115200) # устанавливам BaudRate на 9600
Sound.volume_set(0) # устанавливам звук на 0%

comb = QtWidgets.QComboBox()



# действия при открытом порте
def onRead():
    if not serial.canReadLine(): return     # выходим если нечего читать
    rx = serial.readLine()
    rxs = str(rx, 'utf-8').strip()
    data = rxs.split(',')
    #print(data)
    Sound.volume_set(int(data[0]))
    ui.lcdM.display(int(data[0]))

    if ui.DialMode.currentText() == "Chrome":
        dial_chrome_set(int(data[1]))
        ui.lcdC.display(int(data[1]))
    elif ui.DialMode.currentText() == "AIMP":
        dial_aimp_set(int(data[1]))
        ui.lcdA.display(int(data[1]))
    elif ui.DialMode.currentText() == "TG / Viber":
        dial_telegram_set(int(data[1]))
        ui.lcdT.display(int(data[1]))
    elif ui.DialMode.currentText() == "Another app":
        dial_app_set(int(data[1]))
        ui.lcdS.display(int(data[1]))

# открыть порт
def onOpen():
    serial.setPortName(ui.comL.currentText())
    serial.open(QIODevice.ReadWrite)

# закрыть порт
def onClose():
    serial.close()

#управление громкостью Chrome
def dial_chrome_set(app_chrome):
    app_chrome = float(app_chrome) / 100
    sessions = AudioUtilities.GetAllSessions()
    ui.lcdC.display(ui.dial_chrome.value())
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        if session.Process and session.Process.name() == "chrome.exe":
          volume.SetMasterVolume(app_chrome, None)

#управление громкостью Aimp
def dial_aimp_set(app_aimp):
    app_aimp = float(app_aimp) / 100
    sessions = AudioUtilities.GetAllSessions()
    ui.lcdA.display(ui.dial_aimp.value())
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        if session.Process and session.Process.name() == "AIMP.exe":
          volume.SetMasterVolume(app_aimp, None)

#управление громкостью Telegram
def dial_telegram_set(app_telegram):
    prog = ui.clo.currentText() + ".exe"
    
    app_telegram = float(app_telegram) / 100
    sessions = AudioUtilities.GetAllSessions()
    ui.lcdT.display(ui.dial_telegram.value())
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        if session.Process and session.Process.name() == prog:
          volume.SetMasterVolume(app_telegram, None)

#управление громкостью приложения на выбор
def dial_app_set(app_app):
    prog = ui.sell.currentText()
    
    app_app = float(app_app) / 100
    sessions = AudioUtilities.GetAllSessions()
    ui.lcdS.display(ui.dial_select.value())
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        if session.Process and session.Process.name() == prog:
          volume.SetMasterVolume(app_app, None)

#заглушить Chrome
def muteSoundC(val): 
    #print(ui.mute_chrome.checkState())
    if ui.mute_chrome.checkState() == 2:
        
        dial_chrome_set(0)
        ui.lcdC.display("--") 
    elif ui.mute_chrome.checkState() == 0:
         
        dial_chrome_set(ui.dial_chrome.value())
        ui.lcdC.display(ui.dial_chrome.value())

#заглушить Telegram
def muteSoundT(val): 
    
    if ui.mute_tg.checkState() == 2:
        
        dial_telegram_set(0)
        ui.lcdT.display("--") 
    elif ui.mute_tg.checkState() == 0:
         
        dial_telegram_set(ui.dial_telegram.value())
        ui.lcdT.display(ui.dial_telegram.value())

#заглушить выбраное приложение
def muteSoundR(val): 
    
    if ui.mute_select.checkState() == 2:
        
        dial_app_set(0)
        ui.lcdS.display("--") 
    elif ui.mute_select.checkState() == 0:
         
        dial_app_set(ui.dial_select.value())
        ui.lcdS.display(ui.dial_select.value())

#заглушить AIMP
def muteSoundA(val): 
    #print(ui.mute_chrome.checkState())
    if ui.mute_aimp.checkState() == 2:
        
        dial_aimp_set(0)
        ui.lcdA.display("--") 
    elif ui.mute_aimp.checkState() == 0:
         
        dial_aimp_set(ui.dial_aimp.value())
        ui.lcdA.display(ui.dial_aimp.value())

#заглушить выход
def muteSound(val): 
    Sound.mute()
        #print(ui.mute_chrome.checkState())
    if ui.mute_main.checkState() == 2:
        ui.lcdM.display("--") 
    elif ui.mute_chrome.checkState() == 0:
        ui.lcdM.display(ui.dial_main.value())

# обновить список портов
def updateList():
    portList = []
    ports = QSerialPortInfo().availablePorts()
    for port in ports: portList.append(port.portName())
    ui.comL.clear()
    ui.comL.addItems(portList)

# обновить список приложений
def updateListApp():
    ui.sell.clear()
    cmd = 'powershell "gps | where {$_.MainWindowTitle } | select Path'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    for line in proc.stdout:
         if not line.decode()[0].isspace():
            rline = line.decode().rstrip()
            line = rline.split('/')
            line = rline.split("\\")
            appList = str(line[len(line)-1])
            if appList == "Path":i = 0
            elif appList == "----": i = 3
            elif appList == "AIMP.exe": i = 3
            elif appList == "chrome.exe": i = 3
            elif appList == "Telegram.exe": i = 3
            elif appList == "Viber.exe": i = 3
            elif appList == "ApplicationFrameHost.exe": i = 3
            else:ui.sell.addItem(appList)

#управление громкостью звука крутилка      
def setSoundDial():
    #print(ui.dial_main.value()) # DeBug элемента Dial
    Sound.volume_set(ui.dial_main.value())
    ui.lcdM.display(ui.dial_main.value())

#управление громкостью Chrome крутилка
def dial_chrome_preset():
    dial_chrome_set(ui.dial_chrome.value())

#управление громкостью Telegram крутилка
def dial_telegram_preset():
    dial_telegram_set(ui.dial_telegram.value())

#управление громкостью AIMP крутилка
def dial_aimp_preset():
    dial_aimp_set(ui.dial_aimp.value())

#управление громкостью выбраного приложения крутилка
def dial_r_preset():
    dial_app_set(ui.dial_select.value())
    
#кнопка reset 
def res_funk():
    updateList()
    updateListApp()



# пошла программа
updateListApp()
ui.btn_r.clicked.connect(res_funk)
#ui.clo.currentIndexChanged.connect(funct.tv_val)
serial.readyRead.connect(onRead)
ui.mute_main.stateChanged.connect(muteSound)
ui.mute_select.stateChanged.connect(muteSoundR)
ui.mute_tg.stateChanged.connect(muteSoundT)
ui.mute_aimp.stateChanged.connect(muteSoundA)
ui.mute_chrome.stateChanged.connect(muteSoundC)
ui.openB.clicked.connect(onOpen)
ui.closeB.clicked.connect(onClose)
ui.dial_chrome.valueChanged.connect(dial_chrome_preset)
ui.dial_aimp.valueChanged.connect(dial_aimp_preset)
ui.dial_select.valueChanged.connect(dial_r_preset)
ui.dial_telegram.valueChanged.connect(dial_telegram_preset)
ui.dial_main.valueChanged.connect(setSoundDial)
updateList()

ui.show()
app.exec()