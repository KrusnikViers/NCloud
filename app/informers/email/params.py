class Parameters:
    def __init__(self, server: str, login: str, password: str, period: float):
        self.server = server
        self.login = login
        self.password = password
        self.period = period

    @classmethod
    def from_dict(cls, config: dict):
        return cls(str(config['imap_server']),
                   str(config.get('login', '')),
                   str(config.get('password', '')),
                   float(config.get('period', 30.)))