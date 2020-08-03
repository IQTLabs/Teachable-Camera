"""
Example for using the Adafruit RFM9x Radio bonnet with Raspberry Pi.

Learn Guide: https://learn.adafruit.com/lora-and-lorawan-for-raspberry-pi
Author: Brent Rubell for Adafruit Industries

Adapted for SB Node 1 - LoRa v0.3 7/2020 -EMM

"""
# Import Python System Libraries
import time
# Import Blinka Libraries
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
# Import the SSD1306 module.
import adafruit_ssd1306
# Import RFM9x module/bonnet
import adafruit_rfm9x

deviceID=""
# Button A
btnA = DigitalInOut(board.D5)
btnA.direction = Direction.INPUT
btnA.pull = Pull.UP

# Button B
btnB = DigitalInOut(board.D6)
btnB.direction = Direction.INPUT
btnB.pull = Pull.UP

# Button C
btnC = DigitalInOut(board.D12)
btnC.direction = Direction.INPUT
btnC.pull = Pull.UP

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# 128x32 OLED Display
reset_pin = DigitalInOut(board.D4)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, reset=reset_pin)
# Clear the display.
display.fill(0)
display.show()
width = display.width
height = display.height

# Configure LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0,baudrate=1000000) #keep SPI Baudrate < 2MHz to minimize errors
rfm9x.tx_power = 23

#LoRa paramters defaults - set accordingly
#rfm9x.signal_bandwidth = 125000
#rfm9x.coding_rate = 5
#rfm9x.spreading_factor = 7
#rfm9x.enable_crc = False

print("LoRa parameters - bw: {}Hz cr: {} sf: {} crc: {} tx power: {}dBm"\
.format(rfm9x.signal_bandwidth,rfm9x.coding_rate,rfm9x.spreading_factor,rfm9x.enable_crc,rfm9x.tx_power))

prev_packet=None

while True:

    # draw a box to clear the image
    display.fill(0)
    display.text('IQT Labs StakeOut Box', 0, 0, 1)

    # check for packet rx
    packet = rfm9x.receive()
    pkt="{}".format(packet)
    uuid="ID:{}".format(pkt[12:20]) #Device uuid - SB1_SHORT_DEVICE_ID
    data=pkt[12:].split(' ',3)
    _rssi = rfm9x.last_rssi

    if packet is None:
        display.show()
        #display.text('- Waiting for PKT -', 15, 20, 1)
    else:
        # Display the packet text
        print(pkt)
        print("Rssi: {0} dB".format(_rssi))
        rssi=("ID:{} {}dB".format(pkt[12:20],_rssi))
        #print("ID:{} Type:{} Confidence:{}%".format(data[0],data[1],data[2]))
        display.fill(0)
        prev_packet = packet

        display.text('LoRa: Got Alert! ', 25, 0, 1)
        display.text(rssi, 15,15, 1)
        time.sleep(0.1)

    #Disable buttons for now...
    """
    if not btnA.value:
        # Send Button A
        display.fill(0)
        button_a_data = bytes("Button A!\r\n","utf-8")
        rfm9x.send(button_a_data)
        display.text('Sent Button A!', 25, 15, 1)
    elif not btnB.value:
        # Send Button B
        display.fill(0)
        button_b_data = bytes("Button B!\r\n","utf-8")
        rfm9x.send(button_b_data)
        display.text('Sent Button B!', 25, 15, 1)
    elif not btnC.value:
        # Send Button C
        display.fill(0)
        button_c_data = bytes("Button C!\r\n","utf-8")
        rfm9x.send(button_c_data)
        display.text('Sent Button C!', 25, 15, 1)
    """

    display.show()
    #time.sleep(0.1)
