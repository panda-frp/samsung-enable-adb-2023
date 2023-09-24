from typing import List
import serial
import serial.tools.list_ports as prtlst
from serial.tools import list_ports_common
import time

SERIAL_BAUDRATE = 115200
SERIAL_TIMEOUT = 12

#esta linea analiza los puertos com y el que contenga samsung en su nombre lo toma
def samsung_port():
    ports = prtlst.comports()
    for port in ports:
        for a in port:
            if 'SAMSUNG' in a:
                port = port
                return port[0]

def get_AT_serial(port: str) -> serial.Serial:
    return serial.Serial(port, baudrate=SERIAL_BAUDRATE, timeout=SERIAL_TIMEOUT)


def ATSend(io: serial.Serial, cmd: str) -> bool:
    if not io.isOpen():
        return False
    io.write(cmd.encode())
    time.sleep(0.5)
    ret = io.read_all()

    if b"OK\r\n" in ret:
        return True
    if b"ERROR\r\n" in ret:
        return False
    if ret == b"\r\n":
        return False
    if ret == cmd.encode():
        return True
    if ret == b'':
        return False
    return True

def tryATCmds(io: serial.Serial, cmds: List[str]):
    for i, cmd in enumerate(cmds):
        try:
            res = ATSend(io, cmd)
            if not res:
                print("enviando payload")
        except:
            print(f"Error al enviar el comando {cmd}")    
    try:
        io.close()
    except:
        print("No se puede cerrar correctamente la conexión serie")

def enableADB():
    port = samsung_port()
    io = get_AT_serial(port)
    print("Initial...")
    ATSend(io, "AT+KSTRINGB=0,3\r\n")
    print("Activando ADB...")
    cmds = []
    cmds.append("AT+DUMPCTRL=1,0\r\n")
    cmds.append("AT+DEBUGLVC=0,5\r\n")
    cmds.append("AT+SWATD=0\r\n")
    cmds.append("AT+ACTIVATE=0,0,0\r\n")
    cmds.append("AT+SWATD=1\r\n")
    cmds.append("AT+DEBUGLVC=0,5\r\n")
    cmds.append("AT+PARALLEL=2,0,00000;AT+DEBUGLVC=0,5\r\n")
    tryATCmds(io, cmds)
    print("ADB a sido Activado")
    print("Si no aparece el mensaje de depuración USB, intente desconectar o volver a conectar el cable USB")

if __name__ == "__main__":
    enableADB()
