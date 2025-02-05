import serial.tools.list_ports
import getopt, sys
from datetime import datetime
from pyexcel_ods3 import save_data
from collections import OrderedDict
import requests, time
import threading, platform
from requests.exceptions import HTTPError

try:
    apikeyfile = open("thingspeak-api-key.txt", "r")
    apikey = apikeyfile.read().strip()
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

def alx_thread_fnc(event, filename, port, baudrate, upload):
    serialInst = serial.Serial()
    serialInst.baudrate = baudrate
    serialInst.port = port
    try:
        serialInst.open()
    except serial.serialutil.SerialException as error:
        print( ("Αδυναμία σύνδεσης στη θύρα: (% s).. Έξοδος!") % (port) )
        exit(-2)

    print( ("Αναμονή για δεδομένα μέσω σειριακής θύρας % s με ταχύτητα % s.") % (port, baudrate) )
    
    data = OrderedDict() # from collections import OrderedDict
    data.update({"Δεδομένα": [ ["Ημερομηνία", "Ώρα", "Τιμή", "Κανάλι 0", "Κανάλι 1"] ]})
    curValue0 = curValue1 = ''
    
    while True:
        packet = serialInst.readline().decode('utf').rstrip('\n').strip()
        print(getDate() + " " + getTime() + " Δεδομένα: " + packet + " | Πάτησε Enter για να σταματήσει η καταγραφή")
        if (packet[1]==':'):
            if (packet[0]=='0'): # Κανάλι καταγραφής 0
                curValue0 = float(packet[2:])
                data['Δεδομένα'].append([getDate(), getTime(), '', packet[2:], ''])
                save_data("Καταγραφή_" + filename + ".ods", data)
            if (packet[0]=='1'): # Κανάλι καταγραφής 1
                curValue1 = float(packet[2:])
                data['Δεδομένα'].append([getDate(), getTime(), '', '', packet[2:]])
                save_data("Καταγραφή_" + filename + ".ods", data)                   
            if (curValue0!='' and curValue1!='' and upload): # Αποστολή δεδομένων στο thingspeak
                full_url = url + "&field1=" + str(curValue0) + "&field2=" + str(curValue1)
                try:
                    print('Αποστολή στο thingspeak: ' + full_url)
                    r = requests.get(full_url)
                    r.raise_for_status()
                except HTTPError as http_err:
                    print(f"HTTP error occurred: {http_err}")
                except Exception as err:
                    print(f"Other error occurred: {err}")
                else:   
                    print("Επιτυχημένη αποστολή!")
                curValue0 = curValue1 = ''
        else: # Δεν υπάρχει αριθμός και άνω κάτω τελεία => Δεν γίνεται καταγραφή σε κανάλια, δεν γίνεται αποστολή στο thingspeak
            data['Δεδομένα'].append([getDate(), getTime(), packet, '', ''])
            save_data("Καταγραφή_" + filename + ".ods", data)
        if (event.is_set()):
            break        

port = ''
baudrate = 115200 # Default baudrate from Mind+ Arduino
upload = False # Default value - not uploading to Thingspeak
filename = getTimeStamp()

argumentList = sys.argv[1:]
options = "b:p:u"
long_options = ["baudrate=", "port=","upload"]

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
x = threading.Thread(target=alx_thread_fnc, args=(event, filename, port, baudrate, upload))
x.start()
time.sleep(5)
input("")
event.set()