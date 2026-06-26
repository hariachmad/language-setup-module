import os
import socketio
from dotenv import load_dotenv

from infrastructure.SioClient import SioClient
from infrastructure.SioClientWrapper import SioClientWrapper

load_dotenv()
sio = socketio.Client()

if __name__ == '__main__':
    sio_client_instance = SioClient(sio)
    sio_client_wrapper = SioClientWrapper(sio_client_instance)
    sio.connect(os.getenv("SOCKET_IO_SERVER"), auth = {
        "robotId": os.getenv("ROBOT_ID")
    })
    sio.wait()
    
    