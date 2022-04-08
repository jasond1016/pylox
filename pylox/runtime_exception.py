class RuntimeException(Exception):
    def __init__(self, token, message):
        super().__init__(self.message)
        self.message = message
        self.token = token
