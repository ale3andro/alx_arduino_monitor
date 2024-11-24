import dearpygui.dearpygui as dpg
import serial.tools.list_ports
import platform, sys, os

packet = 0
serial_ports = []
values_x = [0]
values_y = []
x_axis_limit = 20
x_axis_increment = 1
shouldOpenSerialPort = False
shouldListenToSerialPort = False
plot_dpg_handle = 0
plot_line_dpg_handle = 0
measure_listbox_dpg_handle = 0
x_axis_dpg_handle = y_axis_dpg_handle = 0
window0 = window1 = popup = button_start_monitoring = 0
isSerialContentsText = False

def callback(sender, app_data):
    #print(f"sender is: {sender}")
    #print(f"app_data is: {app_data}")
    global shouldOpenSerialPort
    global shouldListenToSerialPort
    global isSerialContentsText
    if (sender==button_exit):
        if (dpg.get_item_configuration(button_exit)['label']=='Έξοδος'):
            dpg.stop_dearpygui()
        elif (dpg.get_item_configuration(button_exit)['label']=='Διακοπή'):
            shouldListenToSerialPort = False
            dpg.configure_item(button_exit, label="Έξοδος")

    elif (sender==button_start_monitoring):
        dpg.configure_item("modal_id", show=False) 
        if (dpg.get_item_configuration(button_exit)['label']=='Έξοδος'):
            dpg.configure_item(button_exit, label="Διακοπή")
            if (shouldOpenSerialPort==False):
                isSerialContentsText = False
                # Αλλαγή κλίμακας άξονα y
                if (dpg.get_value(measure_listbox_dpg_handle)[0]=='1'):
                    dpg.set_value(label1, "Θερμοκρασία")
                    dpg.set_axis_limits(y_axis_dpg_handle, -10, 50)    
                elif (dpg.get_value(measure_listbox_dpg_handle)[0]=='2'):
                    dpg.set_value(label1, "Υγρασία Περιβάλλοντος")
                    dpg.set_axis_limits(y_axis_dpg_handle, 0, 110)
                elif (dpg.get_value(measure_listbox_dpg_handle)[0]=='3'):
                    isSerialContentsText = True
                dpg.configure_item(plot_dpg_handle, label=dpg.get_value(label1))
                shouldOpenSerialPort = True
        else:
            dpg.configure_item(button_exit, label="Έξοδος")
            shouldListenToSerialPort = False

    elif (sender==button_checkSerial):
        serial_ports = scanSerialPorts()
        dpg.configure_item(listbox_ports, items=serial_ports)
        if len(serial_ports)==0:
            dpg.configure_item(button_start_monitoring, enabled=False)
        else:
            dpg.configure_item(button_start_monitoring, enabled=True)
    
    elif (sender==button_select_serial_port):
        if (not shouldListenToSerialPort):
            dpg.configure_item("modal_id", show=True)
         
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

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

dpg.create_context()
dpg.create_viewport(title='ale3andro\'s Arduino Serial Monitor (v.0.2)', width=830, height=450, resizable= False)
with dpg.font_registry():
    with dpg.font(resource_path("Ubuntu.ttf"),20) as font1:
        dpg.add_font_range(0x0370, 0x03FF)
    with dpg.font(resource_path("Ubuntu.ttf"),28) as font2:
        dpg.add_font_range(0x0370, 0x03FF)
    with dpg.font(resource_path("Ubuntu.ttf"),50) as font3:
        dpg.add_font_range(0x0370, 0x03FF)
dpg.setup_dearpygui()

with dpg.window(label="", width=300, height=450, no_move=True, no_title_bar=True, no_resize=True, pos=[0, 0]):
    window0 = dpg.last_item()
    label3 = dpg.add_text("Θέλω να μετρήσω:")
    measure_listbox_dpg_handle = dpg.add_listbox(["0.Αναλογικές τιμές (max:1024)", "1.Θερμοκρασία (min:-10, max:50)", "2.Υγρασία (max:110%)", "3.Κείμενο (χωρίς γράφημα)"], width=285, num_items=4)
    spacer0 = dpg.add_text("")
    label1 = dpg.add_input_text(default_value='Περιέχομενα Σειριακής', width=285)
    spacer1 = dpg.add_text("")
    
    label2 = dpg.add_text("0")
    spacer2 = dpg.add_text("")
    with dpg.group(horizontal=True) as group2:
        button_select_serial_port  = dpg.add_button(label="Επιλογή θύρας", width=140, callback=callback)
        with dpg.popup(dpg.last_item(), modal=True, no_move=True, min_size=[200,200], tag="modal_id"):
            popup = dpg.last_item()
            serial_ports = scanSerialPorts()
            label0 = dpg.add_text("Διαθέσιμες Arduino θύρες")
            listbox_ports = dpg.add_listbox(items=serial_ports, num_items=2)
            with dpg.group(horizontal=True) as group2_0:
                button_start_monitoring = dpg.add_button(label="Έναρξη", width=195, callback=callback)
                button_checkSerial  = dpg.add_button(label="Έλεγχος θυρών", width=195, callback=callback)
        button_exit  = dpg.add_button(label="Έξοδος", width=140, callback=callback)
        if len(serial_ports)==0:
            dpg.configure_item(button_start_monitoring, enabled=False)
        else:
            dpg.configure_item(button_start_monitoring, enabled=True)

with dpg.window(label="", width=530, height=450, no_move=True, no_title_bar=True, no_resize=True, pos=[300, 0]):
    window1 = dpg.last_item()
    with dpg.plot(label="Περιεχόμενα Σειριακής", height=430, width=520, tag="alx_plot"):
        plot_dpg_handle = dpg.last_item()
        dpg.add_plot_axis(dpg.mvXAxis, label="Άξονας x")
        x_axis_dpg_handle = dpg.last_item()
        dpg.set_axis_limits(x_axis_dpg_handle, 0, x_axis_limit)
        dpg.add_plot_axis(dpg.mvYAxis, label="Άξονας y", tag="y_axis")
        y_axis_dpg_handle = dpg.last_item()
        dpg.set_axis_limits(dpg.last_item(), 0, 1024)
        dpg.add_line_series([1], [512], label="Φ", parent="y_axis", tag="series_tag")
        plot_line_dpg_handle = dpg.last_item()

    dpg.bind_font(font1)
    dpg.bind_item_font(label0, font2)
    dpg.bind_item_font(spacer0, font2)
    dpg.bind_item_font(spacer1, font2)
    dpg.bind_item_font(label1, font2)
    dpg.bind_item_font(label2, font3)
    dpg.bind_item_font(label3, font2)

with dpg.theme() as disabled_theme:
    with dpg.theme_component(dpg.mvButton, enabled_state=False):
        dpg.add_theme_color(dpg.mvThemeCol_Text, [255, 255, 255])
        dpg.add_theme_color(dpg.mvThemeCol_Button, [255, 10, 10])
dpg.bind_theme(disabled_theme)
dpg.show_viewport()

# below replaces, start_dearpygui()
while dpg.is_dearpygui_running():
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
            dpg.set_value(label2, packet)
            if (not isSerialContentsText):
                if ('.' in packet):
                    values_y.append(int(packet[:packet.rfind('.')]))
                else:
                    values_y.append(int(packet))
                limit = int(x_axis_limit/x_axis_increment)
                if (len(values_x) < (x_axis_limit/x_axis_increment)):
                    dpg.set_value(plot_line_dpg_handle, [values_x, values_y])
                else:
                    dpg.set_value(plot_line_dpg_handle, [values_x[-1*limit:], values_y[-1*limit:]])
                    if (values_x[int(-1*limit/2)] > dpg.get_axis_limits(x_axis_dpg_handle)[1]/2):
                        dpg.set_axis_limits(x_axis_dpg_handle, values_x[-10], values_x[-10] + x_axis_limit)
                values_x.append(values_x[-1] + x_axis_increment)

    dpg.render_dearpygui_frame()

dpg.destroy_context()
