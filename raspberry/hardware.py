import time
import board
import neopixel
from hardware_config import buzzerPin, GPIO


class HardwareController:
    
    def __init__(self):
        self.pixels = None    
        try:
            self.pixels = neopixel.NeoPixel(
                board.D18,
                8, 
                brightness=1.0/32, 
                auto_write=False
            )
            self.pixels.fill((0, 0, 0))
            self.pixels.show()
        except Exception as e:
            print(f"exception occured while led init: {e}")
            self.pixels = None
    
    def buzzer_beep(self, count, duration, pause):
        for _ in range(count):
            GPIO.output(buzzerPin, GPIO.LOW) #on   
            time.sleep(duration) #beep time
            GPIO.output(buzzerPin, GPIO.HIGH) #of
            if count > 1:
                time.sleep(pause) #pause time
    
    def led_animation(self, color, blinks=2, duration=0.3, pause=0.1):
        if self.pixels is None:
            return
        
        try:
            for _ in range(blinks):
                self.pixels.fill(color)
                self.pixels.show()
                time.sleep(duration)
                
                self.pixels.fill((0, 0, 0))
                self.pixels.show()
                if blinks > 1:
                    time.sleep(pause)
        except Exception as e:
            print(f"exception occurred while led animation: {e}")
    
    def signal_success(self):
        self.buzzer_beep(count=1, duration=0.15, pause=0.1)
        self.led_animation(color=(0, 255, 0), blinks=2, duration=0.3, pause=0.1)
    
    def signal_error(self):
        self.buzzer_beep(count=2, duration=0.1, pause=0.1)
        self.led_animation(color=(255, 0, 0), blinks=2, duration=0.2, pause=0.1)
    
    def cleanup(self):
        if self.pixels is not None:
            self.pixels.fill((0, 0, 0))
            self.pixels.show()
        GPIO.output(buzzerPin, GPIO.HIGH) #of
        GPIO.cleanup()