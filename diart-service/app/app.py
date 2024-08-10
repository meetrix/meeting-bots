import asyncio
import websockets

async def handle_websocket(websocket, path):
    print(f"Connection established with {websocket.remote_address}")

    try:
        async for message in websocket:
            # Log when a message is received
            print(f"Received a message of size {len(message)} bytes from {websocket.remote_address}")

            # Here you could process the message as needed
            # For now, we'll just acknowledge the receipt
            await websocket.send("Message received")

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
