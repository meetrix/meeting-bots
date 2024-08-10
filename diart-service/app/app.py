from io import BytesIO
from diart.sources import TorchStreamAudioSource
from diart import SpeakerDiarization
from diart.inference import StreamingInference
import ffmpeg
import asyncio
import websockets
import torchaudio

# Example function to convert WebM data to WAV in memory and process it
def process_webm_data(webm_data):
    # Convert WebM to WAV in memory
    wav_data, _ = (
        ffmpeg
        .input('pipe:0', format='webm')
        .output('pipe:1', format='wav')
        .run(input=webm_data, capture_stdout=True, capture_stderr=True)
    )

    # Use BytesIO to simulate a file in memory
    wav_io = BytesIO(wav_data)

    # Initialize the StreamReader from torchaudio
    streamer = torchaudio.io.StreamReader(wav_io, format='wav')

    # Extract sample rate from the WAV data
    sample_rate = streamer.get_src_stream_info(0).sample_rate

    # Initialize the TorchStreamAudioSource with the StreamReader
    source = TorchStreamAudioSource(uri="in_memory_wav", sample_rate=sample_rate, streamer=streamer)

    # Initialize the Speaker Diarization pipeline
    pipeline = SpeakerDiarization()

    # Create the Streaming Inference instance
    inference = StreamingInference(pipeline, source)

    # Run the prediction
    prediction = inference()

    # For demonstration, print the prediction (if any)
    print(prediction)

# Example usage in the WebSocket server
async def handle_websocket(websocket, path):
    print(f"Connection established with {websocket.remote_address}")

    try:
        async for message in websocket:
            print(f"Received a message of size {len(message)} bytes from {websocket.remote_address}")
            process_webm_data(message)
            await websocket.send("Message processed")

    except websockets.exceptions.ConnectionClosed as e:
        print(f"Connection closed: {e}")
    except Exception as e:
        print(f"Error: {e}")

    finally:
        print(f"Connection with {websocket.remote_address} closed.")

# Example WebSocket server setup
async def main():
    server = await websockets.serve(handle_websocket, "0.0.0.0", 7007)
    print("WebSocket server listening on ws://0.0.0.0:7007")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
