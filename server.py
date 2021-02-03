import logging
import asyncio
import grpc
from typing import Iterable

import streamcount_pb2
import streamcount_pb2_grpc


class StreamCounterService(streamcount_pb2_grpc.StreamCounter):

    async def Count(self,
                    request_iterator: Iterable[streamcount_pb2.CountRequest],
                    context: grpc.aio.ServicerContext
                    ) -> streamcount_pb2.CountReply:
        users = set()
        async for request in request_iterator:
            # uncomment this to fix the bug
            # users.add(request.user); continue
            users.append(request.user)
        return streamcount_pb2.CountReply(count=len(users))


async def serve() -> None:
    server = grpc.aio.server()
    streamcount_pb2_grpc.add_StreamCounterServicer_to_server(
        StreamCounterService(), server)
    listen_addr = '[::]:50052'
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(serve())
    except KeyboardInterrupt:
        print('user quit')
