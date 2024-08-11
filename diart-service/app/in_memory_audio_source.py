from diart.sources import AudioSource
from rx.subject import Subject
import numpy as np

class InMemoryAudioSource(AudioSource):
    """
    Represents an in-memory source of audio data that can be fed programmatically.

    Parameters
    ----------
    sample_rate: int
        Sample rate of the chunks emitted.
    """

    def __init__(self, sample_rate: int):
        super().__init__(uri="in_memory_audio", sample_rate=sample_rate)
        self.is_closed = False

    def feed_data(self, pcm_data: bytes):
        """
        Feed raw PCM data into the audio stream.

        Parameters
        ----------
        pcm_data: bytes
            The raw PCM audio data to be fed into the stream.
        """
        if self.is_closed:
            raise RuntimeError("Audio source is closed. No more data can be fed.")

        try:
            # Convert PCM bytes to numpy array
            audio_array = np.frombuffer(pcm_data, dtype=np.float32)

            # Reshape the audio array to match the expected format (1, num_samples)
            audio_array = audio_array.reshape(1, -1)

            print(f"Received audio data: {audio_array.shape}")

            # Emit the audio data through the stream
            self.stream.on_next(audio_array)

        except Exception as e:
            self.stream.on_error(e)
            raise

    def read(self):
        """Start reading the source and yielding samples through the stream."""
        # In this case, the stream is controlled externally via `feed_data()`,
        # so we don't need to do anything here.
        pass

    def close(self):
        """Close the in-memory audio source."""
        if not self.is_closed:
            self.is_closed = True
            self.stream.on_completed()
