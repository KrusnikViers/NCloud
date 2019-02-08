class Notification:
    # Notification type constants
    EMAIL = 10

    def __init__(self, notification_type: int, params: dict, error_string: str = ""):
        self.type = notification_type
        self.params = params
        self.error_string = error_string
