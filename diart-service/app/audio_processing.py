# audio_processing.py

from io import BytesIO
import ffmpeg
import torchaudio
from diart.sources import TorchStreamAudioSource
from diart import SpeakerDiarization
from diart.inference import StreamingInference

def process_webm_data(webm_data):
    """
    Process the WebM data by converting it to WAV in memory and running speaker diarization.

    Parameters:
    - webm_data (bytes): The WebM audio data.

    Returns:
    - str: A string representation of the diarization result.
    """
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

    # Returning the prediction as a string (you may want to format this differently)
    return str(prediction)
