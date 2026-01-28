from enum import Enum
import time
from datetime import datetime
from raspberry.app_config import COOLDOWN_TIME
from checkpoint_id_manager import get_or_create_checkpoint_id
from hardware import HardwareController
from rfid_reader import RFIDReader
from backend_client import BackendClient
from hardware_config import buttonGreen, GPIO

class Mode(Enum):
    CHECKPOINT = "checkpoint"
    REGISTER_RUNNER = "register_runner"

class CheckpointScanner:

    def __init__(self, checkpoint_id):
        self.checkpoint_id = checkpoint_id
        self.hardware = HardwareController()
        self.rfid = RFIDReader()
        self.backend = BackendClient()
        self.last_scanned_cards = {}  # uid -> timestamp of last scan
        self.current_mode = Mode.CHECKPOINT

        self.hardware.display_checkpoint_id(checkpoint_id)

        GPIO.add_event_detect(
            buttonGreen, 
            GPIO.FALLING, 
            callback=self._toggle_mode_callback, 
            bouncetime=300
        )
    
    def _toggle_mode_callback(self, channel):
        if self.current_mode == Mode.CHECKPOINT:
            self.current_mode = Mode.REGISTER_RUNNER
        else:
            self.current_mode = Mode.CHECKPOINT

    def is_card_in_cooldown(self, uid):
        if uid in self.last_scanned_cards:
            time_since_last_scan = time.time() - self.last_scanned_cards[uid] 
            return time_since_last_scan < COOLDOWN_TIME
        return False
    
    def process_card_checkpoint(self, uid):
        timestamp = datetime.now().isoformat()
        
        success = self.backend.send_checkpoint_data(
            self.checkpoint_id, 
            uid, 
            timestamp
        )
        
        if success:
            self.hardware.signal_success_checkpoint()
        else:
            self.hardware.signal_error()
        
        self.last_scanned_cards[uid] = time.time() #dict[uid] is always up to date
        
        return success
    
    def process_card_register_runner(self, uid):
        success = self.backend.create_runner(uid)
        
        if success:
            self.hardware.signal_success_register_runner()
        else:
            self.hardware.signal_error()
        
        self.last_scanned_cards[uid] = time.time()  #dict[uid] is always up to date

        return success
    
    def process_card(self, uid):
        if self.current_mode == Mode.CHECKPOINT:
            return self.process_card_checkpoint(uid)
        elif self.current_mode == Mode.REGISTER_RUNNER:
            return self.process_card_register_runner(uid)

    def run(self):
        try:
            while True:
                uid = self.rfid.read_card_uid()
                
                if uid is not None:
                    if not self.is_card_in_cooldown(uid):
                        self.process_card(uid)
                
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\n\nkeyboard interrupt")
        finally:
            self.hardware.cleanup()
            print("good bye :)")


def main():
    checkpoint_id = get_or_create_checkpoint_id()
    
    if not checkpoint_id:
        return 1
    
    scanner = CheckpointScanner(checkpoint_id)
    scanner.run()
    
    return 0


if __name__ == "__main__":
    exit(main())    