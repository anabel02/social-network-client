# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/follow_service.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from proto import db_models_pb2 as proto_dot_db__models__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1aproto/follow_service.proto\x12\rsocialnetwork\x1a\x15proto/db_models.proto\"<\n\x11\x46ollowUserRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t\x12\x16\n\x0etarget_user_id\x18\x02 \x01(\t\"\x14\n\x12\x46ollowUserResponse\">\n\x13UnfollowUserRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t\x12\x16\n\x0etarget_user_id\x18\x02 \x01(\t\"\x16\n\x14UnfollowUserResponse\"&\n\x13GetFollowingRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t\">\n\x14GetFollowingResponse\x12&\n\tfollowing\x18\x01 \x03(\x0b\x32\x13.socialnetwork.User2\x94\x02\n\rFollowService\x12Q\n\nFollowUser\x12 .socialnetwork.FollowUserRequest\x1a!.socialnetwork.FollowUserResponse\x12W\n\x0cUnfollowUser\x12\".socialnetwork.UnfollowUserRequest\x1a#.socialnetwork.UnfollowUserResponse\x12W\n\x0cGetFollowing\x12\".socialnetwork.GetFollowingRequest\x1a#.socialnetwork.GetFollowingResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'proto.follow_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_FOLLOWUSERREQUEST']._serialized_start=68
  _globals['_FOLLOWUSERREQUEST']._serialized_end=128
  _globals['_FOLLOWUSERRESPONSE']._serialized_start=130
  _globals['_FOLLOWUSERRESPONSE']._serialized_end=150
  _globals['_UNFOLLOWUSERREQUEST']._serialized_start=152
  _globals['_UNFOLLOWUSERREQUEST']._serialized_end=214
  _globals['_UNFOLLOWUSERRESPONSE']._serialized_start=216
  _globals['_UNFOLLOWUSERRESPONSE']._serialized_end=238
  _globals['_GETFOLLOWINGREQUEST']._serialized_start=240
  _globals['_GETFOLLOWINGREQUEST']._serialized_end=278
  _globals['_GETFOLLOWINGRESPONSE']._serialized_start=280
  _globals['_GETFOLLOWINGRESPONSE']._serialized_end=342
  _globals['_FOLLOWSERVICE']._serialized_start=345
  _globals['_FOLLOWSERVICE']._serialized_end=621
# @@protoc_insertion_point(module_scope)
