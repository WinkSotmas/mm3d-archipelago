class ArchipelagoClient:
    """Minimal skeleton for Archipelago client integration.

    Will be extended to use the official Archipelago client library to
    handle multiworld connections, item/flag handling, and slot logic.
    """

    def __init__(self, server: str, slot: str):
        self.server = server
        self.slot = slot
        self.client = None

    def connect(self):
        # TODO: integrate with archipelago-client library
        print(f"[archipelago] would connect to {self.server} as {self.slot}")

    def disconnect(self):
        # TODO: gracefully disconnect
        print("[archipelago] disconnect (stub)")
