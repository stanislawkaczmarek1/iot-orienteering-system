import requests
from raspberry.app_config import BACKEND_URL, BACKEND_TIMEOUT


class BackendClient:
    def __init__(self, backend_url=BACKEND_URL):
        self.backend_url = backend_url
    
    def send_checkpoint_data(self, checkpoint_id, rfid_uid, timestamp):
        data = {
            "checkpoint_id": checkpoint_id,
            "rfid_uid": rfid_uid,
            "timestamp": timestamp
        }
        
        try:
            response = requests.post(
                self.backend_url,
                json=data,
                headers={'Content-Type': 'application/json'},
                timeout=BACKEND_TIMEOUT
            )
            
            if response.status_code == 200 or response.status_code == 201:
                return True
            else:
                print("wrong response status code")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"excepion occured while sending request: {e}")
            return False
