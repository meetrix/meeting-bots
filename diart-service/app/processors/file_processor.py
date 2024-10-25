import sys
from pathlib import Path
import torchaudio
import numpy as np
from diart import SpeakerDiarization
from diart.inference import StreamingInference
from app.sources.in_memory_audio_source import InMemoryAudioSource

def process_audio_file(file_path, sample_rate=16000):
    """
    Process a local audio file and run speaker diarization.

    Parameters:
    - file_path (str or Path): The path to the audio file.
    - sample_rate (int): The sample rate to use for processing.

    Returns:
    - str: A string representation of the diarization result.
    """
    try:
        # Convert file_path to a Path object if it's not already
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Load the audio file into memory using torchaudio
        waveform, original_sample_rate = torchaudio.load(file_path)

        # Resample if necessary
        if original_sample_rate != sample_rate:
            resampler = torchaudio.transforms.Resample(orig_freq=original_sample_rate, new_freq=sample_rate)
            waveform = resampler(waveform)

        # Convert the waveform to PCM data (int16) and then to bytes
        pcm_data = waveform.numpy().astype(np.float32).tobytes()

        # Initialize the InMemoryAudioSource with the sample rate
        source = InMemoryAudioSource(sample_rate=sample_rate)

        # Feed the PCM data into the InMemoryAudioSource
        source.feed_data(pcm_data)

        # Initialize the Speaker Diarization pipeline
        pipeline = SpeakerDiarization()

        # Create the Streaming Inference instance
        inference = StreamingInference(pipeline, source)

        # Run the prediction
        prediction = inference()

        print(f"Speaker Diarization prediction for {file_path}:")
        print(prediction)

        # Return the prediction as a string
        return str(prediction)

    except Exception as e:
        print(f"Error processing audio file: {e}")
        raise
