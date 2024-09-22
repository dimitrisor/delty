import grpc
from concurrent import futures
from django.core.management import call_command
from django.conf import settings
from grpc_reflection.v1alpha import reflection

# Import the generated gRPC code
from delty_grpc import track_content_difference_pb2, track_content_difference_pb2_grpc


class TrackContentDifferenceServicer(
    track_content_difference_pb2_grpc.TrackContentDifferenceServiceServicer
):
    def TriggerTrackContentDifference(self, request, context):
        try:
            call_command("track_content_difference")
            return track_content_difference_pb2.TriggerResponse(
                success=True, message="Command executed successfully"
            )
        except Exception as e:
            return track_content_difference_pb2.TriggerResponse(
                success=False, message=str(e)
            )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    track_content_difference_pb2_grpc.add_TrackContentDifferenceServiceServicer_to_server(
        TrackContentDifferenceServicer(), server
    )

    # Add reflection service
    SERVICE_NAMES = (
        track_content_difference_pb2.DESCRIPTOR.services_by_name[
            "TrackContentDifferenceService"
        ].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    server.add_insecure_port(f"[::]:{settings.GRPC_PORT}")
    print(f"Starting gRPC server on port {settings.GRPC_PORT}...")
    server.start()
    server.wait_for_termination()
