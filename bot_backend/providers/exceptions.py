class ProviderNotSupported(Exception):
    def __init__(self):
        super().__init__("Provider is not supported")
