import dearpygui.dearpygui as dpg
import serial.tools.list_ports
import random

packet = 0
serial_ports = []
values_x = [0]
values_y = []
x_axis_limit = 20
x_axis_increment = 1
shouldOpenSerialPort = False
shouldListenToSerialPort = False
plot_dpg_handle = 0
x_axis_dpg_handle = 0

def callback(sender, app_data):
    #print(f"sender is: {sender}")
    #print(f"app_data is: {app_data}")
    if (sender==button_exit):
        dpg.stop_dearpygui()
    elif (sender==button_run):
        #print(dpg.get_value(listbox_ports))
        #print(dpg.get_item_configuration(listbox_ports))
        global shouldOpenSerialPort
        global shouldListenToSerialPort
        if (dpg.get_item_configuration(button_run)['label']=='Έναρξη'):
            dpg.configure_item(button_run, label="Διακοπή")
            if (shouldOpenSerialPort==False):
                shouldOpenSerialPort = True
            
            startListening(dpg.get_value(listbox_ports))
        else:
            dpg.configure_item(button_run, label="Έναρξη")
            shouldListenToSerialPort = False

    elif (sender==button_checkSerial):
        serial_ports = scanSerialPorts()
        dpg.configure_item(listbox_ports, items=serial_ports)
        if len(serial_ports)==0:
            dpg.configure_item(button_run, enabled=False)
        else:
            dpg.configure_item(button_run, enabled=True)
        
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
                        port = boards_descriptions[j] + " | " + '/dev/' + value.name
                #print('Εντοπίστηκε Arduino στη θύρα:', port)
                arduino_ports.append(port)
    return arduino_ports

def startListening(port):
    return

serial_ports = scanSerialPorts()

dpg.create_context()
dpg.create_viewport(title='Arduino Serial Monitor', width=425, height=800, resizable= False)
with dpg.font_registry():
    with dpg.font("font/Ubuntu.ttf",20) as font1:
        dpg.add_font_range(0x0370, 0x03FF)
    with dpg.font("font/Ubuntu.ttf",28) as font2:
        dpg.add_font_range(0x0370, 0x03FF)
    with dpg.font("font/Ubuntu.ttf",50) as font3:
        dpg.add_font_range(0x0370, 0x03FF)
dpg.setup_dearpygui()

with dpg.window(label="", width=425, height=800, no_move=True, no_title_bar=True, no_resize=True, pos=[0, 0]):
    label0 = dpg.add_text("Διαθέσιμες Arduino θύρες")
    listbox_ports = dpg.add_listbox(items=serial_ports, num_items=2)
    spacer0 = dpg.add_text("")

    button_checkSerial  = dpg.add_button(label="Έλεγχος θυρών", width=200, callback=callback)

    label1 = dpg.add_input_text(default_value='Περιέχομενα Σειριακής')
    spacer1 = dpg.add_text("")
    
    label2 = dpg.add_text("0")
    spacer2 = dpg.add_text("")
    with dpg.group(horizontal=True) as group2:
        button_run  = dpg.add_button(label="Έναρξη", width=200, callback=callback)
        button_exit  = dpg.add_button(label="Έξοδος", width=200, callback=callback)
   
    with dpg.plot(label="Φωτεινότητα", height=400, width=400, tag="alx_plot"):
        # optionally create legend
        dpg.add_plot_legend()

        # REQUIRED: create x and y axes
        dpg.add_plot_axis(dpg.mvXAxis, label="x")
        x_axis_dpg_handle = dpg.last_item()
        dpg.set_axis_limits(x_axis_dpg_handle, 0, x_axis_limit)
        dpg.add_plot_axis(dpg.mvYAxis, label="y", tag="y_axis")
        dpg.set_axis_limits(dpg.last_item(), 0, 1024)

        dpg.add_line_series([1, 2, 3], [10, 20, 30], label="Φ", parent="y_axis", tag="series_tag")

    plot_dpg_handle = dpg.last_item()

    if len(serial_ports)==0:
        dpg.configure_item(button_run, enabled=False)
    dpg.bind_font(font1)
    dpg.bind_item_font(label0, font2)
    dpg.bind_item_font(spacer0, font2)
    dpg.bind_item_font(spacer1, font2)
    dpg.bind_item_font(label1, font2)
    dpg.bind_item_font(label2, font3)

    #print(dpg.get_item_configuration(x_axis_dpg_handle))

dpg.show_viewport()

# below replaces, start_dearpygui()
while dpg.is_dearpygui_running():
    # insert here any code you would like to run in the render loop
    # you can manually stop by using stop_dearpygui()
    #print("this will run every frame")
    if shouldOpenSerialPort:
        serialInst = serial.Serial(timeout=4)
        serialInst.baudrate = 115200
        port = dpg.get_value(listbox_ports)
        serialInst.port = port[port.find('|')+2:].strip()
        try:
            serialInst.open()
        except serial.serialutil.SerialException as error:
            print( ("Αδυναμία σύνδεσης στη θύρα: (% s).. Έξοδος!") % (port) )
            dpg.stop_dearpygui()
            exit(-2)
        shouldOpenSerialPort = False
        shouldListenToSerialPort = True
        
    if shouldListenToSerialPort:
        packet = serialInst.readline().decode('utf').rstrip('\n').strip()
        if packet:
            #print("Δεδομένα: " + packet)
            dpg.set_value(label2, packet)
            values_y.append(int(packet))
            limit = int(x_axis_limit/x_axis_increment)
            if (len(values_x) < (x_axis_limit/x_axis_increment)):
                dpg.set_value(plot_dpg_handle, [values_x, values_y])
            else:
                dpg.set_value(plot_dpg_handle, [values_x[-1*limit:], values_y[-1*limit:]])
                if (values_x[int(-1*limit/2)] > dpg.get_axis_limits(x_axis_dpg_handle)[1]/2):
                    dpg.set_axis_limits(x_axis_dpg_handle, values_x[-10], values_x[-10] + x_axis_limit)
            values_x.append(values_x[-1] + x_axis_increment)

            '''
            if (len(values_x)>1000):
                values_x = values_x[-1000:]
                values_y = values_y[-1000:]
            dpg.set_value(plot, [values_x, values_y])
            values_x.append(values_x[-1] + x_axis_increment)
            if (values_x[-1]>=x_axis_limit):
                values_x = [0]
                values_y = []
            '''
    
    

    dpg.render_dearpygui_frame()

dpg.destroy_context()
