# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/auth_service.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from proto import db_models_pb2 as proto_dot_db__models__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x18proto/auth_service.proto\x12\rsocialnetwork\x1a\x15proto/db_models.proto\"2\n\x0cLoginRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"\x1e\n\rLoginResponse\x12\r\n\x05token\x18\x01 \x01(\t\"2\n\rSignUpRequest\x12!\n\x04user\x18\x01 \x01(\x0b\x32\x13.socialnetwork.User\"\x10\n\x0eSignUpResponse2\x91\x01\n\x04\x41uth\x12\x42\n\x05Login\x12\x1b.socialnetwork.LoginRequest\x1a\x1c.socialnetwork.LoginResponse\x12\x45\n\x06SignUp\x12\x1c.socialnetwork.SignUpRequest\x1a\x1d.socialnetwork.SignUpResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'proto.auth_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_LOGINREQUEST']._serialized_start=66
  _globals['_LOGINREQUEST']._serialized_end=116
  _globals['_LOGINRESPONSE']._serialized_start=118
  _globals['_LOGINRESPONSE']._serialized_end=148
  _globals['_SIGNUPREQUEST']._serialized_start=150
  _globals['_SIGNUPREQUEST']._serialized_end=200
  _globals['_SIGNUPRESPONSE']._serialized_start=202
  _globals['_SIGNUPRESPONSE']._serialized_end=218
  _globals['_AUTH']._serialized_start=221
  _globals['_AUTH']._serialized_end=366
# @@protoc_insertion_point(module_scope)
