import uuid
from typing import List
import grpc.aio
import logging
from rpc.client import create_channel, FOLLOW, POST, USER
from store import Storage
from proto.follow_service_pb2 import FollowUserRequest
from proto.posts_service_pb2 import CreatePostRequest
from proto.users_service_pb2 import EditUserRequest
from proto.follow_service_pb2_grpc import FollowServiceStub
from proto.users_service_pb2_grpc import UserServiceStub
from proto.posts_service_pb2_grpc import PostServiceStub


logger = logging.getLogger(__name__)


class Request:
    def __init__(self, service: int, request):
        self.id = str(uuid.uuid4())
        self.service = service
        self.request = request


def add_request(request: Request):
    requests: List = Storage.disk_get('requests', [])
    requests.append(request)
    Storage.disk_store('requests', requests)


def get_requests() -> List[Request]:
    return Storage.disk_get('requests', [])


def remove_request(request: Request):
    requests: List[Request] = Storage.disk_get('requests', [])
    try:
        requests = [r for r in requests if r.id != request.id]
        requests.remove(request)
    except ValueError:
        pass
    Storage.disk_store('requests', requests)


def clear_requests():
    Storage.disk_store('requests', [])


async def process_requests():
    requests = get_requests()
    logger.info(f"Processing requests: {requests}")
    processed = []

    for request in requests:
        logger.info(f"Processing request: {request}")
        response = None
        try:
            if request.service == FOLLOW:
                async with await create_channel(FOLLOW) as channel:
                    stub = FollowServiceStub(channel)
                    if isinstance(request.request, FollowUserRequest):
                        response = await stub.FollowUser(request.request)
                    else:
                        logger.info(f"Unknown FOLLOW request offline: {request.request}")

            if request.service == POST:
                async with await create_channel(POST) as channel:
                    stub = PostServiceStub(channel)
                    if isinstance(request.request, CreatePostRequest):
                        response = await stub.CreatePost(request.request)
                    else:
                        logger.info(f"Unknown POST request offline: {request.request}")

            if request.service == USER:
                async with await create_channel(USER) as channel:
                    stub = UserServiceStub(channel)
                    if isinstance(request.request, EditUserRequest):
                        response = await stub.EditUser(request.request)
                    else:
                        logger.info(f"Unknown USER request offline: {request.request}")

            else:
                logger.info(f"Unknown service: {request.service}")

        except grpc.aio.AioRpcError as e:
            logger.error(f"gRPC error in {request.service}.{request.request}: {e.code()}; {e.details()}")
            continue
        except Exception as err:
            logger.exception(f"Request processing failed with exception: {err}")
            continue

        if response is not None:
            processed.append(request)
            logger.info(f"Request processed successfully: {request}")
        else:
            logger.warning(f"Request processing did not yield a response: {request}")

    for req in processed:
        remove_request(req)

    logger.info(f"Processed {len(processed)} requests")
