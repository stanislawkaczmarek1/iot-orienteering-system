from mfrc522 import MFRC522


class RFIDReader:

    def __init__(self):
        self.reader = MFRC522()
    
    def read_card_uid(self):
        (status, TagType) = self.reader.MFRC522_Request(self.reader.PICC_REQIDL)
        
        if status == self.reader.MI_OK:
            (status, uid) = self.reader.MFRC522_Anticoll()
            if status == self.reader.MI_OK:
                uid_number = 0
                for i in range(0, len(uid)):
                    uid_number += uid[i] << (i*8)
                return uid_number
        return None

