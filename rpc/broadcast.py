import socket
import logging
from store import Storage

BROADCAST_PORT = 11000


def discover():
    broadcast = '255.255.255.255'
    logging.info(f"Discovering on {broadcast}")
    # udp broadcast on broadcast address
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(1)
    sock.sendto(b"Are you a chord?", (broadcast, BROADCAST_PORT))
    response = None
    address = None
    while True:
        try:
            logging.info("Waiting for response")
            response, address = sock.recvfrom(1024)
            logging.info(f"Received {response} from {address}")
            if response.startswith(b"Yes, I am a chord"):
                yield address[0]
        except socket.timeout:
            logging.info("Timeout")
            break
        except BaseException as e:
            logging.info(f"Error: {e}")
            break
    try:
        sock.close()
    except BaseException as e:
        logging.info(f"Error closing socket: {e}")
    logging.info("No more servers found")


def update_servers():
    servers = list(discover())
    logging.info(f"Found servers: {servers}")
    if servers:
        logging.info("Updating servers")
        Storage.store('server', servers)
    else:
        logging.info("No servers found")
        Storage.delete('server')
