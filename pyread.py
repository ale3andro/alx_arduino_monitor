import serial.tools.list_ports
from pprint import pprint
import getopt, sys
from pynput import keyboard
from datetime import datetime
from pyexcel_ods3 import save_data
from collections import OrderedDict
import requests
import threading, platform

try:
    apikeyfile = open("thingspeak-api-key.txt", "r")
    apikey = apikeyfile.read()
    print("Thingspeak api key:", apikey)
except IOError:
    exit("Αδυναμία ανοίγματος αρχείου thingspeak-api-key.txt")

url = 'https://api.thingspeak.com/update?api_key=' + apikey

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

def scanSerialPorts():
    boards = ['1A86:7523', '2341:0043'] # The first is R2 Uno board and the 2nd is the S1 board
    boards_descriptions = ["R2", "S1"]
    ports = list(serial.tools.list_ports.comports())
    arduino_ports = []
    for index, value in enumerate(sorted(ports)):
        for i in boards:
            if (i in value.hwid):
                for j in range(len(boards)):
                    if i==boards[j]:
                        if (platform.system()=='Linux'):
                            port = boards_descriptions[j] + " | " + '/dev/' + value.name
                        else:
                            port = boards_descriptions[j] + " | " + value.name
                arduino_ports.append(port)
    return arduino_ports

def alx_thread_fnc(event, port, baudrate, upload):
    serialInst = serial.Serial()
    serialInst.baudrate = baudrate
    serialInst.port = port
    try:
        serialInst.open()
    except serial.serialutil.SerialException as error:
        print( ("Αδυναμία σύνδεσης στη θύρα: (% s).. Έξοδος!") % (port) )
        exit(-2)

    print( ("Αναμονή για δεδομένα μέσω σειριακής θύρας % s με ταχύτητα % s. Για τερματισμό πάτησε το πλήκτρο ESC.") % (port, baudrate) )
    
    filename = getTimeStamp()
    data = OrderedDict() # from collections import OrderedDict
    data.update({"Δεδομένα": [ ["Ημερομηνία", "Ώρα", "Τιμή", "Κανάλι 0", "Κανάλι 1"] ]})
    
    while True:
        packet = serialInst.readline().decode('utf').rstrip('\n').strip()
        print(getDate() + " " + getTime() + " Δεδομένα: " + packet)
        if (packet[1]==':'):
            if (packet[0]=='0'): # Κανάλι καταγραφής 0
                curValue0 = float(packet[2:])
                data['Δεδομένα'].append([getDate(), getTime(), '', packet[2:], ''])
            if (packet[0]=='1'): # Κανάλι καταγραφής 1
                curValue1 = float(packet[2:])
                data['Δεδομένα'].append([getDate(), getTime(), '', '', packet[2:]])                    
            if (curValue0!='' and curValue1!='' and upload): # Αποστολή δεδομένων στο thingspeak
                full_url = url + "&field1=" + str(curValue0) + "&field2=" + str(curValue1)
                r = requests.get(full_url)
                print('Αποστολή στο thingspeak: ' + full_url)
                curValue0 = curValue1 = ''
        else: # Δεν υπάρχει αριθμός και άνω κάτω τελεία => Δεν γίνεται καταγραφή σε κανάλια, δεν γίνεται αποστολή στο thingspeak
            data['Δεδομένα'].append([getDate(), getTime(), packet, '', ''])
        if (event.is_set()):
            break
    
    save_data("Καταγραφή_" + filename + ".ods", data)

        

port = ''
baudrate = 115200 # Default baudrate from Mind+ Arduino
upload = False # Default value - not uploading to Thingspeak

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

if port=='':
    port=scanSerialPorts()
    if (len(port)==0):
        print('Δεν βρέθηκαν συνδεδεμένα Arduino S1 ή R2 στον Υπολογιστή.')
        exit()
    elif (len(port)==1):
        port = port[0][port[0].find('|')+2:].strip()
        print(port)
    else:
        print('Bρέθηκαν περισσότερα από ένα συνδεδεμένα Arduino S1 ή R2 στον Υπολογιστή.')
        exit()

print(port, baudrate, upload)
event = threading.Event()
x = threading.Thread(target=alx_thread_fnc, args=(event, port, baudrate, upload))
x.start()
input("Press Enter to stop monitoring")
event.set()