import requests
from app_config import BACKEND_CHECKPOINT_URL, BACKEND_CREATE_RUNNER_URL, BACKEND_TIMEOUT


class BackendClient:
    def __init__(self):
        self.checkpoint_url = BACKEND_CHECKPOINT_URL
        self.runner_url = BACKEND_CREATE_RUNNER_URL
    
    def send_checkpoint_data(self, checkpoint_id, rfid_uid, timestamp):
        data = {
            "checkpoint_id": checkpoint_id,
            "rfid_uid": rfid_uid,
            "timestamp": timestamp
        }
        
        try:
            response = requests.post(
                self.checkpoint_url,
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
            print(f"excepion occurred while sending request: {e}")
            return False
        
    def create_runner(self, rfid_uid):
        data = {
            "rfid_uid": rfid_uid
        }
        
        try:
            response = requests.post(
                self.runner_url,
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
            print(f"excepion occurred while sending request: {e}")
            return False
