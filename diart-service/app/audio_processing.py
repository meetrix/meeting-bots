import numpy as np
import torchaudio
import torch
from io import BytesIO
from diart.sources import TorchStreamAudioSource
from diart import SpeakerDiarization
from diart.inference import StreamingInference

def process_pcm_data(pcm_data, sample_rate=48000):
    """
    Process raw PCM data and run speaker diarization.

    Parameters:
    - pcm_data (bytes): The raw PCM audio data.
    - sample_rate (int): The sample rate of the audio data.

    Returns:
    - str: A string representation of the diarization result.
    """
    try:
        # Log data type and shape
        print("Received PCM data type:", type(pcm_data))
        print("PCM data length:", len(pcm_data))

        # Convert PCM bytes to numpy array
        audio_array = np.frombuffer(pcm_data, dtype=np.float32)
        print("Converted audio array shape:", audio_array.shape)

        # Reshape the audio array to match the expected format (1, num_samples)
        audio_array = audio_array.reshape(1, -1)

        # Use BytesIO to simulate a file in memory
        wav_io = BytesIO()
        # Save the NumPy array as a WAV file using torchaudio's save function
        torchaudio.save(wav_io, torch.from_numpy(audio_array), sample_rate, format='wav')
        wav_io.seek(0)

        # Initialize the StreamReader from torchaudio
        streamer = torchaudio.io.StreamReader(wav_io, format='wav')

        # Initialize the TorchStreamAudioSource with the StreamReader
        source = TorchStreamAudioSource(uri="in_memory_wav", sample_rate=sample_rate, streamer=streamer, stream_index=0)

        # Initialize the Speaker Diarization pipeline
        pipeline = SpeakerDiarization()

        # Create the Streaming Inference instance
        inference = StreamingInference(pipeline, source)

        # Run the prediction
        prediction = inference()

        print("Speaker Diarization prediction:")
        print(prediction)

        # Return the prediction as a string
        return str(prediction)
    
    except Exception as e:
        print(f"Error processing PCM data: {e}")
        raise
