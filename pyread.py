import serial.tools.list_ports
from pprint import pprint
import getopt, sys
import keyboard
from datetime import datetime
from pyexcel_ods3 import save_data
from collections import OrderedDict
import requests

url = 'https://api.thingspeak.com/update?api_key=XZ4WW4NQTJVLQCJD'

def getTimeStamp():
    timestamp = datetime.now()
    return timestamp.strftime("%Y-%m-%d_%H-%M-%S")

def getDate():
    timestamp = datetime.now()
    return timestamp.strftime("%Y-%m-%d")

def getTime():
    timestamp = datetime.now()
    return timestamp.strftime("%H-%M-%S")

filename = getTimeStamp()

data = OrderedDict() # from collections import OrderedDict
data.update({"Δεδομένα": [ ["Ημερομηνία", "Ώρα", "Τιμή", "Κανάλι 0", "Κανάλι 1"] ]})

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

ports = []
ports = list(serial.tools.list_ports.comports())

if port=='':
    print("Προσπάθεια εντοπισμού συνδεδεμένου Arduino...")
    for index, value in enumerate(sorted(ports)):
        #print(index, '\t', value.name, '\t', value.manufacturer)
        if ('Arduino' in value.manufacturer):
            port = value.name
            print('Εντοπίστηκε Arduino στη θύρα:', port)

serialInst = serial.Serial()
serialInst.baudrate = baudrate
serialInst.port = port
try:
    serialInst.open()
except serial.serialutil.SerialException as error:
    print( ("Αδυναμία σύνδεσης στη θύρα: (% s).. Έξοδος!") % (port) )
    exit(-2)

print( ("Αναμονή για δεδομένα μέσω σειριακής θύρας % s με ταχύτητα % s. Για τερματισμό πάτησε το πλήκτρο q.") % (port, baudrate) )
while True:
    if serialInst.in_waiting:
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
        
        
    if keyboard.is_pressed("q"):
        print("Πατήθηκε το q, τερματισμός καταγραφής δεδομένων σειριακής.")
        save_data("Καταγραφή_" + filename + ".ods", data)
        break