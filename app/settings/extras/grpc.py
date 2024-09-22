from app import env

GRPC_PORT = env.get_int("GRPC_PORT", 50051)
