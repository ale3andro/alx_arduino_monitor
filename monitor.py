import serial.tools.list_ports
from pprint import pprint
import getopt, sys
from pynput import keyboard
from datetime import datetime
import dearpygui.dearpygui as dpg
import threading

listeningSerial=True

def getTimeStamp():
    timestamp = datetime.now()
    return timestamp.strftime("%Y-%m-%d_%H-%M-%S")

def getDate():
    timestamp = datetime.now()
    return timestamp.strftime("%Y-%m-%d")

def getTime():
    timestamp = datetime.now()
    return timestamp.strftime("%H-%M-%S")

def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        print("Πατήθηκε το ESC, τερματισμός καταγραφής δεδομένων σειριακής.")
        global listeningSerial
        listeningSerial=False
        return False
        
dpg.create_context()
dpg.create_viewport(title='My first app', width=400, height=300, resizable= False)
with dpg.font_registry():
    with dpg.font("font/Ubuntu.ttf",20) as font1:
        dpg.add_font_range(0x0370, 0x03FF)
    with dpg.font("font/Ubuntu.ttf",28) as font2:
        dpg.add_font_range(0x0370, 0x03FF)

def callback(sender, app_data):
    print(f"sender is: {sender}")
    print(f"app_data is: {app_data}")
    if (sender==button_exit):
        dpg.destroy_context()
    else:
        print('button_run')
        startMonitoring()

    #dpg.set_value(textInput0, app_data['current_path'])
    #print(dpg.get_value(listbox0))
    
with dpg.window(label="", width=400, height=300, no_move=True, no_title_bar=True, no_resize=True, pos=[0, 0]):
    label0 = dpg.add_text('Περιέχομενα Σειριακής')
    
    spacer0 = dpg.add_text("")
    label1 = dpg.add_text("SERIAL")
    spacer1 = dpg.add_text("")
    with dpg.group(horizontal=True) as group2:
        button_run  = dpg.add_button(label="Εκτέλεση", width=200, callback=callback)
        button_exit  = dpg.add_button(label="Έξοδος", width=200, callback=callback)
    
    dpg.bind_font(font1)
    dpg.bind_item_font(label0, font2)
    dpg.bind_item_font(spacer0, font2)
    dpg.bind_item_font(spacer1, font2)
    dpg.bind_item_font(label1, font2)
    
def updateSerialMessage(msg):
    dpg.set_value(label1, msg)


def startMonitoring():
    boards = ['1A86:7523', '2341:0043'] # The first is R2 Uno board and the 2nd is the S1 board

    port = ''
    baudrate = 115200 # Default baudrate from Mind+ Arduino

    argumentList = sys.argv[1:]
    options = "b:p:u"
    long_options = ["baudrate=", "port=","upload"]

    curValue0 = curValue1 = ''

    try:
        arguments, values = getopt.getopt(argumentList, options, long_options)
        for currentArgument, currentValue in arguments:
            if currentArgument in ("-b", "--baudrate"):
                print (("Ρύθμιση ταχύτητας σύνδεσης σε: (% s)") % (currentValue))
                baudrate = int(currentValue)
            elif currentArgument in ("-p", "--port"):
                print (("Ρύθμιση θύρας σύνδεσης σε: (% s)") % (currentValue))
                port = currentValue
            elif currentArgument in ("-u", "--upload"):
                print ("Αποστολή δεδομένων στο thingspeak")
                upload = True
    except getopt.error as err:
        # output error, and return with an error code
        print (str(err))

    ports = []
    ports = list(serial.tools.list_ports.comports())
    if port=='':
        print("Προσπάθεια εντοπισμού συνδεδεμένου Arduino...")
        for index, value in enumerate(sorted(ports)):
            for i in boards:
                if (i in value.hwid):
                    port = '/dev/' + value.name
                    print('Εντοπίστηκε Arduino στη θύρα:', port)

    #port = '/dev/serial/by-id/usb-1a86_USB_Serial-if00-port0'
    #port = '/dev/ttyUSB0'
    baud = 115200
    serialInst = serial.Serial(timeout=4)
    serialInst.baudrate = baudrate
    serialInst.port = port
    try:
        serialInst.open()
    except serial.serialutil.SerialException as error:
        print( ("Αδυναμία σύνδεσης στη θύρα: (% s).. Έξοδος!") % (port) )
        exit(-2)

    print( ("Αναμονή για δεδομένα μέσω σειριακής θύρας % s με ταχύτητα % s. Για τερματισμό πάτησε το πλήκτρο ESC.") % (port, baudrate) )


    listener = keyboard.Listener(on_release=on_release)
    listener.start()

    while listeningSerial:
        print('alex')       
        packet = serialInst.readline().decode('utf').rstrip('\n').strip()
        if packet:
            print(getDate() + " " + getTime() + " Δεδομένα: " + packet)
            updateSerialMessage(packet)
        '''
        if (packet[1]==':'):
            if (packet[0]=='0'): # Κανάλι καταγραφής 0
                curValue0 = float(packet[2:])
                data['Δεδομένα'].append([getDate(), getTime(), '', packet[2:], ''])
            if (packet[0]=='1'): # Κανάλι καταγραφής 1
                curValue1 = float(packet[2:])
                data['Δεδομένα'].append([getDate(), getTime(), '', '', packet[2:]])                    
            
        else: # Δεν υπάρχει αριθμός και άνω κάτω τελεία => Δεν γίνεται καταγραφή σε κανάλια, δεν γίνεται αποστολή στο thingspeak
            data['Δεδομένα'].append([getDate(), getTime(), packet, '', ''])
        '''


dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()