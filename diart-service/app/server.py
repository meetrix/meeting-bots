# server.py

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from app.audio_processing import process_pcm_data
from app.file_processor import process_audio_file
from pathlib import Path

# script_dir = Path(__file__).resolve().parent
# audio_file_path = script_dir / "../data/sample.wav"
# process_audio_file(file_path=audio_file_path)

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print(f"Connection established with {websocket.client.host}:{websocket.client.port}")

    try:
        while True:
            message = await websocket.receive_bytes()
            print(f"Received a message of size {len(message)} bytes from {websocket.client.host}:{websocket.client.port}")
            result = process_pcm_data(message)
            await websocket.send_text(result)
    
    except WebSocketDisconnect:
        print(f"Connection with {websocket.client.host}:{websocket.client.port} closed.")
    
    except Exception as e:
        print(f"Error: {e}")
        await websocket.close()
