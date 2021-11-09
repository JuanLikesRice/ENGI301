# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
Pedometer on PocketBeagle using Pedometer 3 Click & SPI LCD Screen
--------------------------------------------------------------------------
Juan Garza
This code was modifed form of https://www.hackster.io/170850/standalone-pedometer-pocketbeagle-mikro-click-boards-d14d93
This code is for engi 301 and is not meant for monetary gain 
Credits to Jennifer Haller, Cathy Wicks, Greg Sheridan for the preios code which was modified
for the pedometer reading and sensor usage


https://www.hackster.io/jag33/engi-301-pedometer-313707

--------------------------------------------------------------------------
Software API:

  * Class Pedometer()
      - Contains all functions for interacting with the pedometer and display 
          click boards:
  * init()
      - Initializes the pedometer and configures/enables the step count engine
  * read_accel()
      - Reads 6 bytes of acceleration data
      - Returns x-, y-, z-acceleration for +/-2g range
  * read_steps()
      - Reads 2 bytes of step count data
      - Returns the integer value
 class BuzzerSound 
    -uses frequency and time the buzzer is on for alerting user
    
 

  * Class attributes:
      - state: tracks the current state of the device (INIT, WAIT, WALK, REST)
      - step_total: tracks the current step total for this exercise
      - time_counter: tracks the amount of time passing for task scheduling
      - sleep_num: the current frame of the sleep animation (1-3)
      - walk_num: the current frame of the walking animation (0-4)
  
  function SPI_display_text()
    -updates the display, uses all the data that will be displayed. 
  
--------------------------------------------------------------------------
Background Information: 
 
  * Using the PocketBeagle:
    * https://github.com/beagleboard/pocketbeagle/wiki/System-Reference-Manual

  * Using the Pedometer 3 Click board from MikroElektronika:
    * https://www.mikroe.com/pedometer-3-click
    * http://kionixfs.kionix.com/en/datasheet/KX126-1063-Specifications-Rev-2.0.pdf
    * http://kionixfs.kionix.com/en/document/AN073-Getting-Started-with-Pedometer.pdf
    * https://github.com/RohmSemiconductor/Arduino/tree/master/KX126

  * Using the OLED C Click board from MikroElektronika:
    * https://www.hackster.io/103416/standalone-magic-8-ball-pocketbeagle-mikro-click-boards-4f1bb4

  * Using the display
    ▪ https://learn.adafruit.com/adafruit-2-8-and-3-2-color-tft-touchscreen-breakout-v2/overview
    ▪ https://learn.adafruit.com/adafruit-2-8-and-3-2-color-tft-touchscreen-breakout-v2/spi-wiring-and-test
    ▪ https://learn.adafruit.com/adafruit-2-8-and-3-2-color-tft-touchscreen-breakout-v2/python-wiring-and-setup
    ▪ https://learn.adafruit.com/adafruit-2-8-and-3-2-color-tft-touchscreen-breakout-v2/python-usage

  * Using the GPIO library:
    * https://github.com/adafruit/Adafruit_Python_GPIO/tree/master/Adafruit_GPIO

--------------------------------------------------------------------------
"""
#for the origial pedometer
import time
import os
from PIL import Image, ImageDraw, ImageFont
import Adafruit_GPIO.I2C as I2C

#for the Display of the pedoneter
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.ili9341 as ili9341
import adafruit_rgb_display.st7789 as st7789  # pylint: disable=unused-import
import adafruit_rgb_display.hx8357 as hx8357  # pylint: disable=unused-import
import adafruit_rgb_display.st7735 as st7735  # pylint: disable=unused-import
import adafruit_rgb_display.ssd1351 as ssd1351  # pylint: disable=unused-import
import adafruit_rgb_display.ssd1331 as ssd1331  # pylint: disable=unused-import

# First define some constants to allow easy resizing of shapes.
BORDER = 20
FONTSIZE = 24
# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.P1_6)
dc_pin = digitalio.DigitalInOut(board.P1_4)
reset_pin = digitalio.DigitalInOut(board.P1_2)
# Config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000
# Setup SPI bus using hardware SPI:
spi = board.SPI()


disp = ili9341.ILI9341(spi,
    rotation=90,  # 2.2", 2.4", 2.8", 3.2" ILI9341
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,)
# pylint: enable=line-too-long
# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
if disp.rotation % 180 == 90:
    height = disp.width  # we swap height/width to rotate it to landscape!
    width = disp.height
else:
    width = disp.width  # we swap height/width to rotate it to landscape!
    height = disp.height
image = Image.new("RGB", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)



# First define some constants to allow easy positioning of text.
padding = -2
#-2
x = 20

# Load a TTF font.  Make sure the .ttf font file is in the
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)



def SPI_display_text(tot_steps, avg_rat, time_counted, state, ins_rat, set_speed, all_steps,tot_time):
    '''
    Use for the display, every Time this Function is used, the screen is updates with the values
    '''
    draw.rectangle((0, 0, width, height), outline=0, fill=(233, 196, 106))
    y = padding
    time_str =      "Loop: " + str(time_counted)
    speedstr =      "Speed Goal SPM: " + str(set_speed)
    step_str =      "Cycle Steps: " + str(tot_steps)
    avg_state_str = "Avg Rate SPM: " + str(round(avg_rat,1))
    state_str =     "Code State: " + str(state)
    ins_rat_str =   "Inst. Rate SPM: " + str(ins_rat)
    all_steps_str = "All Steps: " + str(all_steps)
    
    tot_min = int(tot_time//60)
    tot_sec = round(tot_time%60,1)
    #print(tot_sec)
    t_time_str = "Time: 0" + str(tot_min)+":"+str(tot_sec)
    #to make time display much prettier
    
    draw.text((x, y), time_str, font=font, fill="#0000FF")
    y += font.getsize(time_str)[1]
    
    draw.text((x, y), t_time_str, font=font, fill="#023047")
    y += font.getsize(t_time_str)[1]
    y += font.getsize(time_str)[1]/2
   
    draw.text((x, y), speedstr, font=font, fill="#540b0e")
    y += font.getsize(speedstr)[1]
    
    draw.text((x, y), avg_state_str, font=font, fill="#333d29")
    y += font.getsize(avg_state_str)[1]
    
    draw.text((x, y), step_str, font=font, fill="#001219")
    y += font.getsize(step_str)[1]
    y += font.getsize(step_str)[1]/2
    #draw.text((x, y), state_str, font=font, fill="#540b0e")
    #y += font.getsize(state_str)[1]
    
    draw.text((x, y), ins_rat_str, font=font, fill="#0000FF")
    y += font.getsize(ins_rat_str)[1]
    
    draw.text((x, y), all_steps_str, font=font, fill="#F3500F")
    y += font.getsize(all_steps_str)[1]
    
    
    disp.image(image)



# Assumes I2C2 bus for communication with the pedometer
i2c = I2C.Device(0x1F, 2)

# Register map
KX126_DEVICE_ADDRESS_1F   = 0x1F           # 7bit Addres
KX126_CNTL1               = 0x1A
KX126_CNTL2               = 0x1B
KX126_CNTL3               = 0x1C
KX126_CNTL4               = 0x1D
KX126_CNTL5               = 0x1E
KX126_ODCNTL              = 0x1F
KX126_INC1                = 0x20            # Physical interrupt pin INT1
KX126_INC2                = 0x21            # Axis and direction (motion)
KX126_INC3                = 0x22            # Axis and direction (tap mode)
KX126_INC4                = 0x23            # Interrupt routing to INT1
KX126_INC5                = 0x24            # Physical interrupt pin INT2
KX126_INC6                = 0x25            # Interrupt routing to INT2
KX126_INC7                = 0x26            # Step counter interrupt control
KX126_LPCNTL              = 0x37            # Low power control (# samples averaged)   
# Bit masks for control registers
KX126_CNTL1_TPE           = 0x01            # Tilt engine ("1" enables)
KX126_CNTL1_PDE           = 0x02            # Step counter engine ("1" enables)
KX126_CNTL1_TDTE          = 0x04            # Tap/double tap engine ("1" enables)
KX126_CNTL1_GSELMASK      = 0x18
KX126_CNTL1_GSEL_2G       = 0x00
KX126_CNTL1_GSEL_4G       = 0x08
KX126_CNTL1_GSEL_8G       = 0x10
KX126_CNTL1_DRDYE         = 0x20            # Data ready engine ("1" enables)
KX126_CNTL1_RES           = 0x40            # Resolution ("1" higher)
KX126_CNTL1_PC1           = 0x80
KX126_CNTL2_SRST          = 0x80            # Software reset
KX126_ODCNTL_OSA_50HZ     = 0x02            # Acceleration output data rate (ODRs)
KX126_ODCNTL_OSA_100HZ    = 0x03
# Pedometer control registers (to edit, PC1 in CNTL1 must be cleared)
KX126_PED_WM_L            = 0x41            # Hold watermark threshold for step counting
KX126_PED_WM_H            = 0x42
KX126_PED_CNTL1           = 0x43
KX126_PED_CNTL2           = 0x44
KX126_PED_CNTL3           = 0x45            #
KX126_PED_CNTL4           = 0x46            # Maximum impact from floor
KX126_PED_CNTL5           = 0x47            # Minimum impact from floor
KX126_PED_CNTL6           = 0x48            # Maximum time interval for peak
KX126_PED_CNTL7           = 0x49            # Minimum time interval for peak
KX126_PED_CNTL8           = 0x4A            # Time window for noise and delay
KX126_PED_CNTL9           = 0x4B            # Time interval to prevent overflow
KX126_PED_CNTL10          = 0x4C            # Minimum time for a single stride
RESET_DELAY               = 0.002
# Acceleration registers (represented in 2's complement)
KX126_XOUT_L              = 0x08
KX126_LPCNTL_0            = 0x00             # No averaging
KX126_LPCNTL_2            = 0x10             # 2 samples averaged
KX126_LPCNTL_4            = 0x20
KX126_LPCNTL_8            = 0x30
KX126_LPCNTL_16           = 0x40
KX126_LPCNTL_32           = 0x50
KX126_LPCNTL_64           = 0x60
KX126_LPCNTL_128          = 0x70
# Pedometer step count registers (cleared on a read)
KX126_PED_STEP_L          = 0x0E
# Bit masks
KX126_PED_CNTL1_STPTH_0   = 0x00             # Number of steps to start counting
KX126_PED_CNTL1_STPTH_2   = 0x10 
KX126_PED_CNTL1_STPTH_4   = 0x20 
KX126_PED_CNTL1_STPTH_6   = 0x30 
KX126_PED_CNTL1_STPTH_8   = 0x40 
KX126_PED_CNTL1_STPTH_10  = 0x50 
KX126_PED_CNTL1_STPTH_12  = 0x60 
KX126_PED_CNTL1_STPTH_14  = 0x70
KX126_PED_CNTL2_HPS_1     = 0x00             # Scaling factor for output from high-pass
KX126_PED_CNTL2_HPS_2     = 0x10
KX126_PED_CNTL2_HPS_4     = 0x20
KX126_PED_CNTL2_HPS_8     = 0x30
KX126_PED_CNTL2_HPS_16    = 0x40
KX126_PED_CNTL2_HPS_32    = 0x50
KX126_PED_CNTL2_HPS_64    = 0x60
KX126_PED_CNTL2_HPS_128   = 0x70
KX126_PED_CNTL2_ODR_100   = 0x0C             # Pedometer output data rate select 100Hz
KX126_PED_CNTL2_ODR_50    = 0x06             # 50Hz

# States
INIT = 0
WAIT = 1
MOVE = 2
REST = 3
    
class Pedometer(object):
    
    def __init__(self):
        self.state = INIT
        self.step_total = 0
    # End def
    
    def init(self):
        """ Initialization for the KX126-1063. 
        Default setting is +/- 2g range. 
        """      
        # Software reset
        val = i2c.readU8(KX126_CNTL2)
        i2c.write8(KX126_CNTL2, (val | KX126_CNTL2_SRST))
        # Delay 2 milliseconds
        time.sleep(RESET_DELAY)
        # Enter standby mode
        i2c.write8(KX126_CNTL1, 0x00)
        # Disable interrupts
        i2c.write8(KX126_INC1, 0x00)
        i2c.write8(KX126_INC5, 0x00)
        # Initialize the pedometer engine settings
        self.init_ped()   
        # Output data rate
        val = i2c.readU8(KX126_ODCNTL)
        i2c.write8(KX126_ODCNTL, (val | KX126_ODCNTL_OSA_100HZ))
        # High resolution
        val = i2c.readU8(KX126_CNTL1) # should be 0x00
        i2c.write8(KX126_CNTL1, (val | KX126_CNTL1_RES))
        # Enable pedometer engine
        val = i2c.readU8(KX126_CNTL1) # should be 0x40 (64)
        i2c.write8(KX126_CNTL1, (val | KX126_CNTL1_PDE))
        # Exit standby mode
        val = i2c.readU8(KX126_CNTL1) # should be 0x42 (66) 
        i2c.write8(KX126_CNTL1, (val | KX126_CNTL1_PC1)) 
        val = i2c.readU8(KX126_CNTL1) # should be 0xC2 (194)
        time.sleep(2)
    # End def
    
    def init_ped(self):
        """ Initialization for the pedometer engine settings. See the app note
        on Getting Started with Pedometer. 
        """        
        # Number of internal acceleration samples used by ped engine
        val = i2c.readU8(KX126_LPCNTL)
        i2c.write8(KX126_LPCNTL, (val | KX126_LPCNTL_4))
        # Number of steps before counting
        val = i2c.readU8(KX126_PED_CNTL1)
        i2c.write8(KX126_PED_CNTL1, (val | KX126_PED_CNTL1_STPTH_2))
        # Scaling factor for HPF and output data rate for the pedometer engine
        val = i2c.readU8(KX126_PED_CNTL2)
        i2c.write8(KX126_PED_CNTL2, (val | KX126_PED_CNTL2_HPS_4 | KX126_PED_CNTL2_ODR_100))
        # Scaling factor for internal HPF
        i2c.write8(KX126_PED_CNTL3, 0x17)
        # Maximum impact from floor
        i2c.write8(KX126_PED_CNTL4, 0x1F)
        # Minimum impact from floor (adjust this for sensitivity)
        i2c.write8(KX126_PED_CNTL5, 0x0A)
        # Maximum time interval for the peak
        i2c.write8(KX126_PED_CNTL6, 0x13)
        # Minimum time interval for the peak
        i2c.write8(KX126_PED_CNTL7, 0x0B)
        # Time window for noise and delay time
        i2c.write8(KX126_PED_CNTL8, 0x08)
        # Time interval to prevent overflowing
        i2c.write8(KX126_PED_CNTL9, 0x19)
        # Minimum time interval for a single stride
        i2c.write8(KX126_PED_CNTL10, 0x1C)
    # End def
    
    def read_accel(self):
        """ Reads and returns the raw acceleration data from the KX126. 
        Conversion to g's assumes +/- 2g range.
        """        
        values = i2c.readList(KX126_XOUT_L, 6)
        x_val  = (values[0] << 8) + values[1]
        y_val  = (values[2] << 8) + values[3]
        z_val  = (values[4] << 8) + values[5]
        # Convert to g's (/16284 for 2g range)
        x_val = float(x_val)/16284
        y_val = float(y_val)/16284
        z_val = float(z_val)/16284
        return (x_val, y_val, z_val)
    # End def
    
    def read_steps(self):
        """ Reads and returns the current step count from the KX126. 
        Note that the register clears on read.
        """
        low = i2c.readU8(KX126_PED_STEP_L)
        high = i2c.readU8(KX126_PED_STEP_L+1)
        steps = (high << 8) + low
        #print(steps)
        return steps
    # End def
    
ped = Pedometer()
#initiallize pedometer

class BuzzerSound():
    #
    pin       = None
    def __init__(self, pin):
        self.pin = pin
    def play_tone(self, frequency, length):
        """Plays a given note for a given length."""
        PWM.start(self.pin, 50, frequency)
        time.sleep(length)
    # end def
    
    def end(self):
        PWM.stop(self.pin)
        PWM.cleanup()
    # End def

def buzzerfunc(freq,timeon):
    '''
    fuction for freq and time buzzer is om
    '''
    buzzer = BuzzerSound("P2_1")
    #print("Play tone")
    buzzer.play_tone(freq, timeon)       
    buzzer.end()

import time
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.PWM as PWM

GPIO.setup("P2_2", GPIO.IN)
GPIO.setup("P2_3", GPIO.IN)
GPIO.setup("P2_4", GPIO.IN)
GPIO.setup("P2_6", GPIO.IN)
#initialize the pins

def check_speed(set_speed, avg_speed):
    '''
    fuction to check if the speed is near what is desired
    '''
    if abs (set_speed-avg_speed) > 40:
        return True
    else:
        return False


start_time = time.time()
#initialize the start timerecords time elapsed

#initialize values for the display 
rate = 0
loop_num = 0
avg_rate = 0
set_speed = 0
cycle_steps = 0


while True:
    current_time = time.time()
    elapsed_time = current_time - start_time
    #Time in the loop, updates the time on the pedemeter
    
    #for each button and their uses
    if GPIO.input("P2_2") == GPIO.LOW:
        #blue button for increasing step speed goal
        set_speed += 20
    
    if GPIO.input("P2_3") == GPIO.LOW:
        #red button for decreasing step speed goal
        if set_speed > 0: 
            set_speed -= 10
        else: 
            pass
    if GPIO.input("P2_4") == GPIO.LOW:
        #green Button which resets speed 
        set_speed = 60
        buzzerfunc(300,.5)
        #buzzer to alert if it was pressed

    if GPIO.input("P2_6") == GPIO.LOW:
        #Yellow button which resets speed, time, but not all of the total steps made
        #loop_num = 0
        cycle_steps = 0
        start_time = time.time()
        #rests the time
        buzzerfunc(300,.5)
    else:
        pass
    
    if check_speed(set_speed, avg_rate):
        buzzerfunc(300,.5)#beeps if speed is far
    
    SPI_display_text(cycle_steps, avg_rate, loop_num, ped.state, rate, set_speed, ped.step_total, elapsed_time)   
    #display line
    if elapsed_time > 0:
        avg_rate = cycle_steps/elapsed_time*60
        #average rate is updated
    
    
    time.sleep(1)
    accel = ped.read_accel()

    
    if (ped.state == INIT):
        # Configure the pedometer and initialize attributes
        ped.init()
        ped.sleep_num = 1
        ped.walk_num = 0
        ped.time_counter = 0
        ped.step_total = 0
        ped.state = WAIT
        continue
        
    elif (ped.state == WAIT):
        # Check for steps
        new_steps = ped.read_steps()
        if (new_steps > 0):
            ped.step_total += new_steps         # update the total before state change
            cycle_steps += new_steps #updates cycle steps as well
            ped.sleep_num = 1                   # reset this for next use
            ped.state = MOVE
            continue
        else:
            ped.sleep_num += 1                  # Cycle through images
            if (ped.sleep_num == 4):
                ped.sleep_num = 1
            
    elif(ped.state == MOVE):
        # If not moving, go to REST state
        if ((abs(accel[0]) < 2) and (abs(accel[1]) < 2) and (abs(accel[2]) < 2)):
            ped.time_counter = 0
            ped.state = REST
            continue
        
        else:
            # Increment time counter
            ped.time_counter += 1
            # Display next image in movement animation
            ped.walk_num += 1
            if (ped.walk_num == 5):
                ped.walk_num = 0
            
            # Every 3 seconds, read the step count
            if (ped.time_counter >= 3):
                new_steps = ped.read_steps()
                ped.step_total += new_steps
                cycle_steps += new_steps
                rate = new_steps/ped.time_counter *60/2
                # the instant rate is updated
                ped.time_counter = 0
                # If no new steps in 3 seconds, go to REST state
                if (new_steps == 0):
                    ped.state = REST
        
    elif(ped.state == REST):
        # Display total step count when entering REST state
        if (ped.time_counter == 0):
            new_steps = ped.read_steps()
            ped.step_total += new_steps
            cycle_steps += new_steps
        
        # Check for movement
        new_steps = ped.read_steps()
        if (new_steps > 0):
            ped.step_total += new_steps        # update the total before state change
            cycle_steps += new_steps
            ped.time_counter = 0               # reset this for next use
            
            ped.state = MOVE
            continue
        else:
            ped.time_counter += 1              # increment to track time in REST state
        
        # Reset after a certain amount of inactivity
        if (ped.time_counter >= 30):
            ped.time_counter = 0
            ped.state = WAIT
            continue
        
    else:   # Should never reach this
        ped.state = INIT
        continue
    
    
    loop_num += 1

        