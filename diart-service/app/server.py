# server.py

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from app.audio_processing import handle_websocket
from app.file_processor import process_audio_file
from pathlib import Path

# script_dir = Path(__file__).resolve().parent
# audio_file_path = script_dir / "../data/sample.wav"
# process_audio_file(file_path=audio_file_path)

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await handle_websocket(websocket)
