import gpiod
import time

print(dir(gpiod))
LED_PIN = 18


chip = gpiod.Chip('gpiochip4')
led_line = chip.get_line(LED_PIN)
led_line.request(consumer='LED', type=gpiod.LINE_REQ_DIR_OUT)

try:
    while True:
        # Turn led on
        led_line.set_value(1)
        time.sleep(1) # wait 1 sec
        #turn led off
        led_line.set_value(0)
        time.sleep(1) #w 1sec
except KeyboardInterrupt:
    # Clean up when the user interrupts the script
    led_line.release()
    chip.close()
    
    # :)
