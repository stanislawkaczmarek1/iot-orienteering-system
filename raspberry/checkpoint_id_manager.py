import os
from uuid import uuid4
import requests
from datetime import datetime
from app_config import CHECKPOINT_ID_FILE, BACKEND_REGISTER_CP_URL, BACKEND_REGISTER_TIMEOUT

def load_checkpoint_id():
    if os.path.exists(CHECKPOINT_ID_FILE):
        try:
            with open(CHECKPOINT_ID_FILE, 'r') as f:
                checkpoint_id = f.read().strip()
                if checkpoint_id:
                    return checkpoint_id
        except Exception as e:
            print(f"exception occurred while checkpointid file reading: {e}")
    return None


def save_checkpoint_id(checkpoint_id):
    try:
        with open(CHECKPOINT_ID_FILE, 'w') as f:
            f.write(checkpoint_id)
        return True
    except Exception as e:
        print(f"exception occurred while checkpointid file writing: {e}")
        return False


def register_with_backend():
    checkpoint_id = str(uuid4())
    
    data = {
        "checkpoint_id": checkpoint_id,
        "timestamp": datetime.now().isoformat()
    }
    
    try:
        response = requests.post(
            BACKEND_REGISTER_CP_URL,
            json=data,
            headers={'Content-Type': 'application/json'},
            timeout=BACKEND_REGISTER_TIMEOUT
        )
        
        if response.status_code == 200 or response.status_code == 201:
            save_checkpoint_id(checkpoint_id)
            return checkpoint_id
        else:
            """
            case when post request with checkpoint id failed:
            
            checkpoint still can send standard event reqest using generated uuid
            but backend doesnt have checkpoint id in the db
            """
            print("wrong response status code")
            save_checkpoint_id(checkpoint_id)
            return checkpoint_id
            
    except requests.exceptions.RequestException as e:
        """
            case when post request with checkpoint id failed:
            
            checkpoint still can send standard event reqest using generated uuid
            but backend doesnt have checkpoint id in the db
        """
        print(f"excepion occurred while sending request: {e}")
        save_checkpoint_id(checkpoint_id)
        return checkpoint_id


def get_or_create_checkpoint_id():
    checkpoint_id = load_checkpoint_id()
    
    if checkpoint_id:
        return checkpoint_id
    
    checkpoint_id = register_with_backend()
    
    return checkpoint_id