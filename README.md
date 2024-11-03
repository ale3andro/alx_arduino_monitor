# Arduino logger

## Περί

Ένα python script, το οποίο σκανάρει τις σειριακές θύρες του Υπολογιστή για να εντοπίσει συνδεδεμένο Arduino. 

Μόλις εντοπίσει Arduino, προσπαθεί να διαβάσει τη σειριακή με δεδομένα ταχύτητα.

Σκοπός του script είναι να διαβάζει μετρήσεις από αισθητήρες του Arduino και να τις αποθηκεύει τοπικά στον Υπολογιστή (σε μορφή LibreOffice Spreasheet ods) είτε να τις "ανεβάζει" στο thingspeak.

## Εγκατάσταση

Θα συμπληρωθεί εν καιρώ

## Χρήση

cd alx_arduino_logger

### Linux

source env/Scripts/activate

### Windows

env\Scripts\activate.bat # Ενεργοποίηση python virtual environment

(env) py -m pyread --port=<Σειριακή θύρα> --baudrate==115200 --upload\

Από τα παραπάνω arguments (port, baudrate, upload) υποχρεωτικό δεν είναι κανένα.

Αν δεν δηλωθεί port, γίνεται ανίχνευση αυτόματα, αν δεν δηλωθεί baudrate τότε το default είναι 115200.

Αν δηλωθεί το upload, τότε γίνεται προσπάθεια upload στο API του thingspeak. Θα πρέπει να υπάρχει όμως το αρχείο thingspeak-api-key.txt μέσα στο οποίο υπάρχει το API key του thingspeak.
