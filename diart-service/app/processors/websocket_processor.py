import numpy as np
from fastapi import WebSocket, WebSocketDisconnect
from diart import SpeakerDiarization
from diart.inference import StreamingInference
from app.sources.in_memory_audio_source import InMemoryAudioSource

class WebSocketAudioProcessor:
    def __init__(self, sample_rate=48000):
        self.sample_rate = sample_rate

        # Initialize the InMemoryAudioSource
        self.source = InMemoryAudioSource(sample_rate=self.sample_rate)

        # Initialize the Speaker Diarization pipeline
        self.pipeline = SpeakerDiarization()

        # Create the Streaming Inference instance
        self.inference = StreamingInference(self.pipeline, self.source)

    def process_pcm_data(self, pcm_data):
        """
        Process raw PCM data through the previously set up pipeline.

        Parameters:
        - pcm_data (bytes): The raw PCM audio data.

        Returns:
        - str: A string representation of the diarization result.
        """
        try:
            # Feed the data into the InMemoryAudioSource
            self.source.feed_data(pcm_data)

            # Run the prediction
            prediction = self.inference()

            print("Speaker Diarization prediction:")
            print(prediction)

            # Return the prediction as a string
            return str(prediction)
        
        except Exception as e:
            print(f"Error processing PCM data: {e}")
            raise

async def handle_websocket(websocket: WebSocket):
    """
    Handle the WebSocket connection for processing PCM data.
    
    Parameters:
    - websocket: The WebSocket connection to handle.
    """
    processor = WebSocketAudioProcessor()  # Set up the diarization pipeline and audio source in __init__
    
    await websocket.accept()
    print(f"Connection established with {websocket.client.host}:{websocket.client.port}")

    try:
        while True:
            # Receive PCM data as bytes
            message = await websocket.receive_bytes()
            print(f"Received a message of size {len(message)} bytes from {websocket.client.host}:{websocket.client.port}")

            # Process the received PCM data
            result = processor.process_pcm_data(message)

            # Send the diarization result back to the client
            await websocket.send_text(result)
    
    except WebSocketDisconnect:
        print(f"Connection with {websocket.client.host}:{websocket.client.port} closed.")
        processor.source.close()  # Ensure the audio source is closed properly
    
    except Exception as e:
        print(f"Error: {e}")
        await websocket.close()
        processor.source.close()  # Ensure the audio source is closed in case of error
