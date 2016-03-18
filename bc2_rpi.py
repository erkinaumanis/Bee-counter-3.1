import RPi.GPIO as GPIO
from time import sleep

DATA = 17
CLK = 22
RESET = 27

# How many shift register chips are daisy-chained.
CHIP_COUNT = 3
# Width of data (how many ext lines).
DATA_WIDTH = CHIP_COUNT * 8

# Set RPi.GPIO  to use BCM pinout
GPIO.setmode(GPIO.BCM)

# Define GPIO directions
GPIO.setup(CLK, GPIO.OUT)
GPIO.setup(DATA, GPIO.IN)
GPIO.setup(RESET, GPIO.OUT)

# Counters for incoming and outgoing
outbound = 0
incoming = 0

# Last value
prev = 0

# Infinite loop to read the registers.
while True:
    # Trigger a parallel Load to latch the state of the data lines
    GPIO.output(RESET, False)
    GPIO.output(RESET, True)

    bitmap = 0
    # Loop to read each bit value from the serial out line of the SN74HC165N.
    for i in range(0, DATA_WIDTH):
        bitmap |= GPIO.input(DATA) << i
        GPIO.output(CLK, False)
        GPIO.output(CLK, True)
    
    if prev != bitmap:
        for i in range(0, DATA_WIDTH, 2):

            slotprev = prev >> i & 0b11

            if slotprev == 0b11:

                slotnow = bitmap >> i & 0b11

                if slotnow == 0b10:
                    incoming += 1
                elif slotnow == 0b01:
                    outbound += 1
        print "incoming:", incoming, "outbound:", outbound

    prev = bitmap
    sleep(0.001)
