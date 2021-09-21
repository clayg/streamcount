import logging
import asyncio
import grpc

import streamcount_pb2
import streamcount_pb2_grpc


USERS = [
    'tom',
    'bob',
    'frank',
    'steve',
    'bob',
    'joe',
    'frank',
    'sally',
]


def request_gen():
    for user in USERS:
        yield streamcount_pb2.CountRequest(user=user)


async def run() -> None:
    async with grpc.aio.insecure_channel('localhost:50052') as channel:
        stub = streamcount_pb2_grpc.StreamCounterStub(channel)
        req = stub.Count(request_gen())
        try:
            response = await req
        except grpc.aio.AioRpcError as e:
            # uncomment this to suppress the task error
            # req._async_request_poller.cancel()
            print('error', e.details())
        else:
            print('success', response.count == len(set(USERS)))


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    try:
        asyncio.run(run())
    finally:
        print('done')
