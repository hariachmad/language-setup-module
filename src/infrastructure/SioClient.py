class SioClient:
    _instance = None

    def __new__(cls, sio=None):
        if cls._instance is None:
            if sio is None:
                raise ValueError("sio should not be None")
            cls._instance = super().__new__(cls)
            cls._instance.sio = sio
        return cls._instance

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            raise RuntimeError("SioClient is not initialized")
        return cls._instance