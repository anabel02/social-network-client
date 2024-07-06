# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from proto import posts_service_pb2 as proto_dot_posts__service__pb2

GRPC_GENERATED_VERSION = '1.64.1'
GRPC_VERSION = grpc.__version__
EXPECTED_ERROR_RELEASE = '1.65.0'
SCHEDULED_RELEASE_DATE = 'June 25, 2024'
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    warnings.warn(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in proto/posts_service_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
        + f' This warning will become an error in {EXPECTED_ERROR_RELEASE},'
        + f' scheduled for release on {SCHEDULED_RELEASE_DATE}.',
        RuntimeWarning
    )


class PostServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreatePost = channel.unary_unary(
                '/socialnetwork.PostService/CreatePost',
                request_serializer=proto_dot_posts__service__pb2.CreatePostRequest.SerializeToString,
                response_deserializer=proto_dot_posts__service__pb2.CreatePostResponse.FromString,
                _registered_method=True)
        self.GetPost = channel.unary_unary(
                '/socialnetwork.PostService/GetPost',
                request_serializer=proto_dot_posts__service__pb2.GetPostRequest.SerializeToString,
                response_deserializer=proto_dot_posts__service__pb2.GetPostResponse.FromString,
                _registered_method=True)
        self.Repost = channel.unary_unary(
                '/socialnetwork.PostService/Repost',
                request_serializer=proto_dot_posts__service__pb2.RepostRequest.SerializeToString,
                response_deserializer=proto_dot_posts__service__pb2.RepostResponse.FromString,
                _registered_method=True)
        self.DeletePost = channel.unary_unary(
                '/socialnetwork.PostService/DeletePost',
                request_serializer=proto_dot_posts__service__pb2.DeletePostRequest.SerializeToString,
                response_deserializer=proto_dot_posts__service__pb2.DeletePostResponse.FromString,
                _registered_method=True)
        self.GetUserPosts = channel.unary_unary(
                '/socialnetwork.PostService/GetUserPosts',
                request_serializer=proto_dot_posts__service__pb2.GetUserPostsRequest.SerializeToString,
                response_deserializer=proto_dot_posts__service__pb2.GetUserPostsResponse.FromString,
                _registered_method=True)


class PostServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CreatePost(self, request, context):
        """Create a new post
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetPost(self, request, context):
        """Get a post by its ID
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Repost(self, request, context):
        """Repost an existing post
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeletePost(self, request, context):
        """Delete a post by its ID
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetUserPosts(self, request, context):
        """Get all posts for a specific user
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_PostServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreatePost': grpc.unary_unary_rpc_method_handler(
                    servicer.CreatePost,
                    request_deserializer=proto_dot_posts__service__pb2.CreatePostRequest.FromString,
                    response_serializer=proto_dot_posts__service__pb2.CreatePostResponse.SerializeToString,
            ),
            'GetPost': grpc.unary_unary_rpc_method_handler(
                    servicer.GetPost,
                    request_deserializer=proto_dot_posts__service__pb2.GetPostRequest.FromString,
                    response_serializer=proto_dot_posts__service__pb2.GetPostResponse.SerializeToString,
            ),
            'Repost': grpc.unary_unary_rpc_method_handler(
                    servicer.Repost,
                    request_deserializer=proto_dot_posts__service__pb2.RepostRequest.FromString,
                    response_serializer=proto_dot_posts__service__pb2.RepostResponse.SerializeToString,
            ),
            'DeletePost': grpc.unary_unary_rpc_method_handler(
                    servicer.DeletePost,
                    request_deserializer=proto_dot_posts__service__pb2.DeletePostRequest.FromString,
                    response_serializer=proto_dot_posts__service__pb2.DeletePostResponse.SerializeToString,
            ),
            'GetUserPosts': grpc.unary_unary_rpc_method_handler(
                    servicer.GetUserPosts,
                    request_deserializer=proto_dot_posts__service__pb2.GetUserPostsRequest.FromString,
                    response_serializer=proto_dot_posts__service__pb2.GetUserPostsResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'socialnetwork.PostService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('socialnetwork.PostService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class PostService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CreatePost(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/socialnetwork.PostService/CreatePost',
            proto_dot_posts__service__pb2.CreatePostRequest.SerializeToString,
            proto_dot_posts__service__pb2.CreatePostResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetPost(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/socialnetwork.PostService/GetPost',
            proto_dot_posts__service__pb2.GetPostRequest.SerializeToString,
            proto_dot_posts__service__pb2.GetPostResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def Repost(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/socialnetwork.PostService/Repost',
            proto_dot_posts__service__pb2.RepostRequest.SerializeToString,
            proto_dot_posts__service__pb2.RepostResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def DeletePost(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/socialnetwork.PostService/DeletePost',
            proto_dot_posts__service__pb2.DeletePostRequest.SerializeToString,
            proto_dot_posts__service__pb2.DeletePostResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetUserPosts(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/socialnetwork.PostService/GetUserPosts',
            proto_dot_posts__service__pb2.GetUserPostsRequest.SerializeToString,
            proto_dot_posts__service__pb2.GetUserPostsResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
