class ReturnException(Exception):
    def __init__(self, value):
        super().__init__()
        self.value = value
