class ArgumentError(Exception):
    def __init__(self, invalidargs):
        self.message = 'Invalid argument for this EventType : '+str(invalidargs)

    def __str__(self):
        return self.message


class MissingArgumentError(Exception):
    def __init__(self):
        self.message = 'Missing argument for this EventType'

    def __str__(self):
        return self.message


class BadEventNameError(Exception):
    def __init__(self):
        self.message = 'Event name is not valid, should be the form (E_)[A-Z_]*$'

    def __str__(self):
        return self.message


class MissingAssetError(Exception):
    def __init__(self):
        self.message = 'This ressource is either missing or not loaded.'

    def __str__(self):
        return self.message
