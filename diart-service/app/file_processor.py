import sys
from pathlib import Path
from diart import SpeakerDiarization
from diart.sources import FileAudioSource
from diart.inference import StreamingInference

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

        # Initialize the FileAudioSource with the file path
        source = FileAudioSource(file=file_path, sample_rate=sample_rate)

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
