class InvalidOutputFile(BaseException):
    def __init__(self, message="An invalid CSV result filename or folder was provided"):
        self.message = message
        super().__init__(self.message)
