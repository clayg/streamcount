What is going on?
=================

I'm trying to demonstrate what I think is a bug in the cancel method of gRPC's
python asyncio client.

What should I do?
=================

Start the server::

        $ python server.py
        INFO:root:Starting server on [::]:50052

Run the client::

        $ python client.py
        error Unexpected <class 'AttributeError'>: 'set' object has no attribute 'append'
        ERROR:asyncio:Task exception was never retrieved
        future: <Task finished name='Task-2' coro=<_StreamRequestMixin._consume_request_iterator() done, defined at /home/clayg/.local/share/virtualenvs/grpc-test-ywCqvyqB/lib/python3.8/site-packages/grpc/aio/_call.py:396> exception=ExecuteBatchError('Failed "execute_batch": (<grpc._cython.cygrpc.SendMessageOperation object at 0x7f79a44b00b0>,)')>
        Traceback (most recent call last):
          File "/home/clayg/.local/share/virtualenvs/grpc-test-ywCqvyqB/lib/python3.8/site-packages/grpc/aio/_call.py", line 406, in _consume_request_iterator
            await self._write(request)
          File "/home/clayg/.local/share/virtualenvs/grpc-test-ywCqvyqB/lib/python3.8/site-packages/grpc/aio/_call.py", line 429, in _write
            await self._cython_call.send_serialized_message(serialized_request)
          File "src/python/grpcio/grpc/_cython/_cygrpc/aio/call.pyx.pxi", line 370, in send_serialized_message
          File "src/python/grpcio/grpc/_cython/_cygrpc/aio/callback_common.pyx.pxi", line 147, in _send_message
          File "src/python/grpcio/grpc/_cython/_cygrpc/aio/callback_common.pyx.pxi", line 98, in execute_batch
        grpc._cython.cygrpc.ExecuteBatchError: Failed "execute_batch": (<grpc._cython.cygrpc.SendMessageOperation object at 0x7f79a44b00b0>,)


Is this helpful?
================

If you uncomment line #34 in the client, the error handling seems to suppress
the asyncio ERROR.

But isn't the server is broken?
===============================

Yes, most of my code is broken most of the time during development; when I get
something that works I ship it.  ;)

If you need to see the happy path on the server uncomment line #19.  I'm sure
there's other more reasonable ways a async stream->unary request could throw a
RpcError and need the asyncio task consuming the request_iterator to be
cancelled.
