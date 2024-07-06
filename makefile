.PHONY: proto
proto:
	python -m grpc_tools.protoc -I. --python_out=./grpc --grpc_python_out=./grpc ./proto/*.proto