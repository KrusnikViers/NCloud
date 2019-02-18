class Notification:
    # Notification type constants
    ERROR = 0  # params: { "error": str }
    EMAIL = 10  # params: { "channel": int, "unread_count": int }

    def __init__(self, notification_type: int, params: dict):
        self.type = notification_type
        self.params = params
