class Agent(object):

    # thread safe Agent both interact with web3 and web2.
    def __init__(self, name: str) -> None:
        self.name = name
        # web3
        self.account = None
        self.slave_accounts = []

        # web2
        self.headers = {}
        self.discord = None
        self.twitter = None

    def export_account(self, verbose=False):
        return {}

    def restore_account(self, verbose=False):
        return None
