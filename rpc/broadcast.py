import socket
import logging
import time
from store import Storage
from typing import List

BROADCAST_PORT = 11000


def discover(timeout: int = 5) -> List[str]:
    broadcast = '255.255.255.255'
    logging.info(f"Discovering on {broadcast}")

    servers = []
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(timeout)

    try:
        sock.sendto(b"Are you a chord?", (broadcast, BROADCAST_PORT))  
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response, address = sock.recvfrom(1024)
                logging.info(f"Received {response} from {address}")
                if response.startswith(b"Yes, I am a chord"):
                    if address[0] not in servers:
                        servers.append(address[0])
                        yield address[0]
            except socket.timeout:
                # Timeout for this iteration, continue listening
                continue
    except Exception as e:
        logging.error(f"Error during discovery: {e}")
    finally:
        sock.close()

    if not servers:
        logging.info("No servers found")
    else:
        logging.info(f"Found {len(servers)} servers: {servers}")


def update_servers():
    servers = list(discover())
    logging.info(f"Found servers: {servers}")
    if servers:
        logging.info("Updating servers")
        Storage.store('server', servers)
    else:
        logging.info("No servers found")
        Storage.delete('server')
