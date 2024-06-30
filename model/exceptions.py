class FailedError(Exception):
    def __init__(self):
        super().__init__("Failed")
