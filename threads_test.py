
import threading
import time

def alx_function1(arg):
    while True:
        print('Worker thread running...')
        if (event.is_set()):
            break
    print('Worker closing down')


event = threading.Event()
x = threading.Thread(target=alx_function1, args=(event,))
x.start()
for i in range(6):
    print(i)
    time.sleep(1)
event.set()
