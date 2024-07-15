import socket
import logging
import time
from store import Storage

BROADCAST_PORT = 11000


logger = logging.getLogger(__name__)


def discover(timeout: int = 5):
    broadcast = '255.255.255.255'
    logger.info(f"Discovering on {broadcast}")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(timeout)

    try:
        sock.sendto(b"Are you a chord?;client", (broadcast, BROADCAST_PORT))
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response, address = sock.recvfrom(1024)
                logger.info(f"Received {response} from {address}")
                if response.startswith(b"Yes, I am a chord"):
                    yield address[0]
            except socket.timeout:
                # Timeout for this iteration, continue listening
                continue
    except Exception as e:
        logger.error(f"Error during discovery: {e}")
    finally:
        sock.close()


def update_servers():
    servers = list(discover())
    if servers:
        logger.info(f"Found {len(servers)} servers: {servers}")
        Storage.store('server', servers)
    else:
        logger.info("No servers found")
        Storage.delete('server')
