import spidev
import time
from RPi import GPIO
import os

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(37, GPIO.IN)

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 600000
spi.lsbfirst = False
spi.mode = 0b01
spi.bits_per_word = 8

reset = 0x06
stop = 0x0A
start = 0x08
sdatac = 0x11
rdatac = 0x10
wakeup = 0x02

chset = [0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C]
data_test = 0x7FFFFF
data_check = 0xFFFFFF

def send_command(command):
    spi.xfer([command])
    time.sleep(0.01)

def write_byte(register, data):
    spi.xfer([0x40 | register, 0x00, data])
    time.sleep(0.01)

send_command(wakeup)
send_command(stop)
send_command(reset)
send_command(sdatac)

write_byte(0x14, 0x80) # GPIO
write_byte(0x01, 0x96)
write_byte(0x02, 0xD4)
write_byte(0x03, 0xE0)
write_byte(0x04, 0x00)

for ch in chset:
    write_byte(ch, 0x00)

send_command(rdatac)
send_command(start)

result = [0]*8

print("Reading EEG data...\nPress Ctrl+C to stop.\n")

try:
    while True:
        GPIO.wait_for_edge(37, GPIO.FALLING)
        output = spi.readbytes(27)
        os.system('clear')
        print("EEG Real-Time Visualization (μV)\n" + "-"*40)
        for i in range(8):
            idx = 3 + i*3
            raw = (output[idx] << 16) | (output[idx+1] << 8) | output[idx+2]
            raw = raw if raw < data_test else raw - data_check
            microvolt = round(4.5 * raw * 1000000 / 16777215, 2)
            result[i] = microvolt
            bar = int((microvolt + 100)/5) * "|"
            print(f"CH{i+1}: {str(microvolt).rjust(8)} μV | {bar}")
        time.sleep(0.1)

except KeyboardInterrupt:
    send_command(stop)
    spi.close()
    print("\nStopped EEG acquisition.")
