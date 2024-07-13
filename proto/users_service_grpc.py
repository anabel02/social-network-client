# Generated by the Protocol Buffers compiler. DO NOT EDIT!
# source: proto/users_service.proto
# plugin: grpclib.plugin.main
import abc
import typing

import grpclib.const
import grpclib.client
if typing.TYPE_CHECKING:
    import grpclib.server

import proto.db_models_pb2
import proto.users_service_pb2


class UserServiceBase(abc.ABC):

    @abc.abstractmethod
    async def GetUser(self, stream: 'grpclib.server.Stream[proto.users_service_pb2.GetUserRequest, proto.users_service_pb2.GetUserResponse]') -> None:
        pass

    @abc.abstractmethod
    async def EditUser(self, stream: 'grpclib.server.Stream[proto.users_service_pb2.EditUserRequest, proto.users_service_pb2.EditUserResponse]') -> None:
        pass

    def __mapping__(self) -> typing.Dict[str, grpclib.const.Handler]:
        return {
            '/socialnetwork.UserService/GetUser': grpclib.const.Handler(
                self.GetUser,
                grpclib.const.Cardinality.UNARY_UNARY,
                proto.users_service_pb2.GetUserRequest,
                proto.users_service_pb2.GetUserResponse,
            ),
            '/socialnetwork.UserService/EditUser': grpclib.const.Handler(
                self.EditUser,
                grpclib.const.Cardinality.UNARY_UNARY,
                proto.users_service_pb2.EditUserRequest,
                proto.users_service_pb2.EditUserResponse,
            ),
        }


class UserServiceStub:

    def __init__(self, channel: grpclib.client.Channel) -> None:
        self.GetUser = grpclib.client.UnaryUnaryMethod(
            channel,
            '/socialnetwork.UserService/GetUser',
            proto.users_service_pb2.GetUserRequest,
            proto.users_service_pb2.GetUserResponse,
        )
        self.EditUser = grpclib.client.UnaryUnaryMethod(
            channel,
            '/socialnetwork.UserService/EditUser',
            proto.users_service_pb2.EditUserRequest,
            proto.users_service_pb2.EditUserResponse,
        )
