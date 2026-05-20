import threading
from typing import Callable, Optional


class ArchipelagoClient:
    """Archipelago client wrapper with graceful fallback.

    This class will attempt to use the installed `archipelago-client` package.
    If it's not available, it remains a stub but exposes the same methods
    so the CLI can call them safely.
    """

    def __init__(self, server: str, slot: str):
        self.server = server
        self.slot = slot
        self.client = None
        self._item_callback: Optional[Callable[[int, int], None]] = None
        self._listen_thread: Optional[threading.Thread] = None
        self._running = False

    def connect(self):
        """Try to initialize real archipelago client; otherwise stay stub."""
        try:
            # Try to import the official client package (name may vary by distribution)
            import archipelago.client as ap_client  # type: ignore
            # This is a best-effort example — actual API may differ.
            self.client = ap_client.ArchipelagoClient(self.server, slot=self.slot)
            self.client.connect()
            self._start_listener_thread()
            print(f"[archipelago] connected to {self.server} as {self.slot}")
        except Exception:
            self.client = None
            print("[archipelago] archipelago-client not found or failed to connect; running in stub mode")

    def _start_listener_thread(self):
        if self._listen_thread:
            return
        self._running = True
        self._listen_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self._listen_thread.start()

    def _listen_loop(self):
        # Placeholder loop: in a real client this would read incoming items
        while self._running:
            # In real implementation: block on client.receive() and call callback
            import time
            time.sleep(1)

    def set_item_callback(self, cb: Callable[[int, int], None]):
        """Register a callback called as cb(location_id, item_id)."""
        self._item_callback = cb

    def disconnect(self):
        self._running = False
        if self.client:
            try:
                self.client.disconnect()
            except Exception:
                pass
        print("[archipelago] disconnected (stub/real)")

    def simulate_receive(self, location_id: int, item_id: int):
        """Simulate receiving an item (useful for testing without server)."""
        if self._item_callback:
            self._item_callback(location_id, item_id)
