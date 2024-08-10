# server.py

import asyncio
import websockets
from audio_processing import process_webm_data

async def handle_websocket(websocket, path):
    print(f"Connection established with {websocket.remote_address}")

    try:
        async for message in websocket:
            print(f"Received a message of size {len(message)} bytes from {websocket.remote_address}")
            result = process_webm_data(message)
            await websocket.send(result)

    except websockets.exceptions.ConnectionClosed as e:
        print(f"Connection closed: {e}")
    except Exception as e:
        print(f"Error: {e}")

    finally:
        print(f"Connection with {websocket.remote_address} closed.")

async def main():
    server = await websockets.serve(handle_websocket, "0.0.0.0", 7007)
    print("WebSocket server listening on ws://0.0.0.0:7007")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
