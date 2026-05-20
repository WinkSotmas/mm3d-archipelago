from mm3d_archipelago.archipelago_client import ArchipelagoClient


def test_simulate_receive_triggers_callback():
    client = ArchipelagoClient('testserver', 'slot1')
    received = []

    def cb(loc, it):
        received.append((loc, it))

    client.set_item_callback(cb)
    client.simulate_receive(123, 456)

    assert received == [(123, 456)]
