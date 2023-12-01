#!/usr/bin/env python
from asyncio.events import get_event_loop
from asyncio.futures import Future
from functools import partial
import asyncio
import threading
import websockets
import json
import kafka

def run_consumer(shutdown_flag, clients, lock):
    print("Starting Kafka Consumer.")

    consumer = kafka.KafkaConsumer("WeatherPredictData", bootstrap_servers="kafka:9093")

    for message in consumer:
        value = message.value
        #formatted = json.dumps(value.decode("utf-8"))
        request = json.loads(value)
        formatted = json.dumps(request)
        print(f"Received: {formatted}")
        print(f"Sending {formatted} to {clients}")
        with lock:
         websockets.broadcast(clients, formatted)
            #for client in clients:
                #asyncio.run(client.send(formatted))

    print("Closing Kafka Consumer")

async def handle_connection(clients, lock, connection, path):
    with lock:
        clients.add(connection)

    try:
        await connection.wait_closed()
    finally:
        with lock:
            clients.remove(connection)

async def main():
    shutdown_flag = threading.Event()
    clients = set()
    lock = threading.Lock()

    consumer_thread = threading.Thread(target=run_consumer, args=(shutdown_flag, clients, lock))
    consumer_thread.start()

    print("Starting WebSocket Server.")
    try:
        async with websockets.serve(partial(handle_connection, clients, lock), "0.0.0.0", 5008):
            await asyncio.Future()
    except asyncio.CancelledError:
        pass
    finally:
        shutdown_flag.set()
        consumer_thread.join()

asyncio.run(main())
