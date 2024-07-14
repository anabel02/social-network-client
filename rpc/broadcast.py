import socket
import logging
import time
from store import Storage

BROADCAST_PORT = 11000


def discover(timeout: int = 5):
    broadcast = '255.255.255.255'
    logging.info(f"Discovering on {broadcast}")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(timeout)

    try:
        sock.sendto(b"Are you a chord?;client", (broadcast, BROADCAST_PORT))
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response, address = sock.recvfrom(1024)
                logging.info(f"Received {response} from {address}")
                if response.startswith(b"Yes, I am a chord"):
                    yield address[0]
            except socket.timeout:
                # Timeout for this iteration, continue listening
                continue
    except Exception as e:
        logging.error(f"Error during discovery: {e}")
    finally:
        sock.close()


def update_servers():
    servers = list(discover())
    if servers:
        logging.info(f"Found {len(servers)} servers: {servers}")
        Storage.store('server', servers)
    else:
        logging.info("No servers found")
        Storage.delete('server')
