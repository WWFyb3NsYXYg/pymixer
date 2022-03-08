#pyinstaller --icon=app.ico --noconsole main.py
from __future__ import print_function
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice
from PyQt5.QtGui import QIcon #библиотека для иконки
from Paradoxis import Sound #файл с проэктом
from Paradoxis import Keyboard
import subprocess

valnm = 2


app = QtWidgets.QApplication([])
ui = uic.loadUi("main.sk") # загружаем интерфейс
ui.setWindowTitle("Beta Mixer") # устанавливам название файла
ui.setWindowIcon(QIcon('icon.png')) # устанавливам иконку файла
serial = QSerialPort()
serial.setBaudRate(115200) # устанавливам BaudRate на 115200
Sound.volume_set(0) # устанавливам звук на 0%
ext_data = 0
def onRead():
    if not serial.canReadLine(): return     # выходим если нечего читать
    rx = serial.readLine()
    rxs = str(rx, 'utf-8').strip()
    data = rxs.split(',')
    if data[0] == '1':
        #print(data[1])
        Sound.volume_set(int(data[1]))
        ui.lcdM.display(int(data[1]))
        
    elif data[0] == '2':
        #print(data[1])
        dial_chrome_set(int(data[1]))
        ui.lcdC.display(int(data[1]))
    elif data[0] == '3':
        #print(data[1])
        dial_aimp_set(int(data[1]))
        ui.lcdA.display(int(data[1]))
    elif data[0] == '4':
        #print(data[1])
        dial_app_set(int(data[1]))
        ui.lcdS.display(int(data[1]))
# открыть порт
comb = QtWidgets.QComboBox()
def dial_chrome_set(app_chrome):
    app_chrome = float(app_chrome) / 100
    sessions = AudioUtilities.GetAllSessions()
    ui.lcdC.display(ui.dial_chrome.value())
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        if session.Process and session.Process.name() == "chrome.exe":
          volume.SetMasterVolume(app_chrome, None)
           






def dial_telegram_set(app_telegram):
    prog = ui.clo.currentText() + ".exe"
    
    app_telegram = float(app_telegram) / 100
    sessions = AudioUtilities.GetAllSessions()
    ui.lcdT.display(ui.dial_telegram.value())
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        if session.Process and session.Process.name() == prog:
          volume.SetMasterVolume(app_telegram, None)
            
def dial_app_set(app_app):
    prog = ui.sell.currentText()
    
    app_app = float(app_app) / 100
    sessions = AudioUtilities.GetAllSessions()
    ui.lcdS.display(ui.dial_select.value())
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        if session.Process and session.Process.name() == prog:
          volume.SetMasterVolume(app_app, None)

def dial_aimp_set(app_aimp):
    app_aimp = float(app_aimp) / 100
    sessions = AudioUtilities.GetAllSessions()
    ui.lcdA.display(ui.dial_aimp.value())
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        if session.Process and session.Process.name() == "AIMP.exe":
          volume.SetMasterVolume(app_aimp, None)

def onOpen():
    serial.setPortName(ui.comL.currentText())
    serial.open(QIODevice.ReadWrite)
# закрыть порт
def onClose():
    serial.close()
def muteSoundC(val): 
    #print(ui.mute_chrome.checkState())
    if ui.mute_chrome.checkState() == 2:
        
        dial_chrome_set(0)
        ui.lcdC.display("--") 
    elif ui.mute_chrome.checkState() == 0:
         
        dial_chrome_set(ui.dial_chrome.value())
        ui.lcdC.display(ui.dial_chrome.value())

def muteSoundT(val): 
    
    if ui.mute_tg.checkState() == 2:
        
        dial_telegram_set(0)
        ui.lcdT.display("--") 
    elif ui.mute_tg.checkState() == 0:
         
        dial_telegram_set(ui.dial_telegram.value())
        ui.lcdT.display(ui.dial_telegram.value())

def muteSoundR(val): 
    
    if ui.mute_select.checkState() == 2:
        
        dial_app_set(0)
        ui.lcdS.display("--") 
    elif ui.mute_select.checkState() == 0:
         
        dial_app_set(ui.dial_select.value())
        ui.lcdS.display(ui.dial_select.value())

def muteSoundA(val): 
    #print(ui.mute_chrome.checkState())
    if ui.mute_aimp.checkState() == 2:
        
        dial_aimp_set(0)
        ui.lcdA.display("--") 
    elif ui.mute_aimp.checkState() == 0:
         
        dial_aimp_set(ui.dial_aimp.value())
        ui.lcdA.display(ui.dial_aimp.value())

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
            

def setSoundDial():
    #print(ui.dial_main.value()) # DeBug элемента Dial
    Sound.volume_set(ui.dial_main.value())
    ui.lcdM.display(ui.dial_main.value())

def dial_chrome_preset():
    dial_chrome_set(ui.dial_chrome.value())

def dial_telegram_preset():
    dial_telegram_set(ui.dial_telegram.value())

def dial_aimp_preset():
    dial_aimp_set(ui.dial_aimp.value())

def dial_r_preset():
    dial_app_set(ui.dial_select.value())
    
def res_funk():
    updateList()
    updateListApp()

    
def tv_val():
    #print("SEC")
    i = 8

#sell

updateListApp()
# пошла программа
ui.btn_r.clicked.connect(res_funk)
ui.clo.currentIndexChanged.connect(tv_val)
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
#comb.select_TV.connect(tv_val)
updateList()

ui.show()
app.exec()