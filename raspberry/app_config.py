CHECKPOINT_ID_FILE = "/home/pi/checkpoint_id.conf"

BACKEND_IP = "your-backend-ip"

BACKEND_CHECKPOINT_URL = f"http://{BACKEND_IP}/api/events" 
BACKEND_REGISTER_CP_URL = f"http://{BACKEND_IP}/api/checkpoints" 
BACKEND_CREATE_RUNNER_URL = f"http://{BACKEND_IP}/api/runners"


BACKEND_TIMEOUT = 5  # sec
BACKEND_REGISTER_TIMEOUT = 10  # sec

COOLDOWN_TIME = 3  # sec