import serial.tools.list_ports
from pprint import pprint
import getopt, sys
from pynput import keyboard
from datetime import datetime

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
        
listeningSerial=True
keyboardThreadStarted=False

filename = getTimeStamp()

boards = ['1A86:7523', '2341:0043'] # The first is R2 Uno board and the 2nd is the S1 board

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