import asyncio
import logging
import grpc
from grpc import aio

from server.data.database import engine, AsyncSessionLocal, Base
from server.services.library_service import LibraryService
from server.handlers.library_handler import LibraryHandler
from proto import library_service_pb2_grpc

# -------- Logging setup --------
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
log = logging.getLogger("library-app")

async def serve():
    # Create database schema if not exists
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create a session factory
    async def session_provider():
        async with AsyncSessionLocal() as session:
            yield session

    # Instantiate service with a session
    # Here we create one session per request in handlers
    # For simplicity, we pass a session directly
    async with AsyncSessionLocal() as session:
        service = LibraryService(session)
        handler = LibraryHandler(service)

        # Create gRPC server
        server = aio.server()
        library_service_pb2_grpc.add_LibraryServiceServicer_to_server(handler, server)
        server.add_insecure_port('[::]:50051')

        await server.start()
        log.info("Library gRPC Server started on port 50051")
        await server.wait_for_termination()

if __name__ == "__main__":
    asyncio.run(serve())