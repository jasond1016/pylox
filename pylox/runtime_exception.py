class RuntimeException(Exception):
    def __init__(self, token, message):
        self.message = message
        self.token = token
        super().__init__(self.message)
