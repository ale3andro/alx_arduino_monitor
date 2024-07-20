


window.onload = (event) => {
    let ports = eel.listArduinoPorts();
    console.log(ports);
};


function button_clicked() {
    let ports = eel.listArduinoPorts();
    console.log(ports);
}