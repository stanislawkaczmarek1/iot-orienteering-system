import time
import board
import os
import neopixel
from hardware_config import buzzerPin, GPIO
from PIL import Image, ImageDraw, ImageFont
import lib.oled.SSD1331 as SSD1331


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
            print(f"exception occurred while led init: {e}")
            self.pixels = None
        
        self.oled = None
        try:
            os.system("sudo systemctl stop ip-oled.service")
            self.oled = SSD1331.SSD1331()
            self.oled.Init()
            self.oled.clear()
        except Exception as e:
            print(f"exception occurred while oled init: {e}")
            self.oled = None
    
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
            self.pixels = neopixel.NeoPixel(
                board.D18,
                8, 
                brightness=1.0/32, 
                auto_write=False
            )

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
    
    def signal_success_checkpoint(self):
        self.buzzer_beep(count=1, duration=0.15, pause=0.1)
        self.led_animation(color=(0, 255, 0), blinks=2, duration=0.3, pause=0.1)
    
    def signal_success_register_runner(self):
        self.buzzer_beep(count=1, duration=0.15, pause=0.1)
        self.led_animation(color=(0, 0, 255), blinks=2, duration=0.3, pause=0.1)
    
    def signal_error(self):
        self.buzzer_beep(count=2, duration=0.1, pause=0.1)
        self.led_animation(color=(255, 0, 0), blinks=2, duration=0.2, pause=0.1)
    
    def cleanup(self):
        if self.pixels is not None:
            self.pixels.fill((0, 0, 0))
            self.pixels.show()
        if self.oled is not None:
            self.oled.clear()
        GPIO.output(buzzerPin, GPIO.HIGH) #of
        GPIO.cleanup()

    def display_checkpoint_id(self, checkpoint_id):
        if self.oled is None:
            return
        
        try:
            short_id = checkpoint_id[:8]
            
            image = Image.new("RGB", (self.oled.width, self.oled.height), "BLACK")
            draw = ImageDraw.Draw(image)
            
            fontSmall = ImageFont.truetype('./lib/oled/Font.ttf', 13)
            fontLarge = ImageFont.truetype('./lib/oled/Font.ttf', 20)
            
            draw.text((8, 5), "Checkpoint:", font=fontSmall, fill="WHITE")
            draw.text((8, 30), short_id, font=fontLarge, fill="GREEN")
            
            self.oled.ShowImage(image, 0, 0)
            
        except Exception as e:
            print(f"exception occurred while oled display: {e}")