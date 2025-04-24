import soundcard as sc
import numpy as np
import serial
import time


#puerto y baudios de arduino
arduino = serial.Serial('COM3', 9600)
time.sleep(2)
#Variables globales
datos = np.zeros((512, 2))
volumen_derecho = 0
volumen_izquierdo = 0

#Funcion limitadora de variables
def limitar_variable(valor, minimo, maximo):
    return max(minimo, min(valor, maximo))


#Captura de audio
mics = sc.all_microphones(include_loopback=True)
for mic in mics:
    print(mic.name)
disp_captura = mics[0]
with disp_captura.recorder(samplerate=44100, channels=2, blocksize=250) as recorder:
    while True:
        start = time.perf_counter()
        datos = recorder.record(numframes=100)
        recorder.flush()
        tiempo_record = time.perf_counter()-start

        start = time.perf_counter()
        rms_der = np.sqrt(np.mean(datos[:, 1]**2))*0.8
        rms_izq = np.sqrt(np.mean(datos[:, 0]**2))*0.8
        tiempo_rms = time.perf_counter()-start

        start = time.perf_counter()
        db_der = 20 * np.log10(rms_der + 1e-6)
        db_izq = 20 * np.log10(rms_izq + 1e-6)
        #db_der = np.clip(db_der, -40, 0) / 40
        #db_izq = np.clip(db_izq, -40, 0) / 40
        nivel_der = (db_der + 40) / 40
        nivel_izq = (db_izq + 40) / 40
        nivel_pwm_der = int(nivel_der * 255)
        nivel_pwm_izq = int(nivel_izq * 255)
        tiempo_db = time.perf_counter()-start

        
        start = time.perf_counter()
        arduino.write(f"{nivel_pwm_der},{nivel_pwm_izq}\n".encode())
        tiempo_usb = time.perf_counter()-start
        print(f"Tiempo de record: {tiempo_record} Tiempo rms: {tiempo_rms} Tiempo db: {tiempo_db} Tiempo usb: {tiempo_usb}")
        time.sleep(0.02)
    