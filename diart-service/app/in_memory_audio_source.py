from diart.sources import AudioSource
from rx.subject import Subject
import numpy as np

class InMemoryAudioSource(AudioSource):
    """
    Represents an in-memory audio source that chunks audio data into blocks of consistent size.
    """

    def __init__(self, sample_rate: int, block_duration: float = 0.5, padding: tuple = (0, 0)):
        super().__init__(uri="in_memory", sample_rate=sample_rate)
        self.block_size = int(np.rint(block_duration * sample_rate))
        self.padding_start, self.padding_end = padding
        self.stream = Subject()
        self.buffer = []

    def feed_data(self, pcm_data: bytes):
        """
        Feed PCM data into the audio source.

        Parameters:
        - pcm_data (bytes): The raw PCM audio data.
        """
        try:
            # Convert PCM bytes to numpy array using float32 (since it's coming from waveform)
            audio_array = np.frombuffer(pcm_data, dtype=np.float32)

            # Add zero padding at the beginning if required
            if self.padding_start > 0:
                num_pad_samples = int(np.rint(self.padding_start * self.sample_rate))
                zero_padding = np.zeros(num_pad_samples, dtype=np.float32)
                audio_array = np.concatenate([zero_padding, audio_array])

            # Buffer the audio data
            self.buffer.extend(audio_array)

            # Process the buffered data in chunks
            while len(self.buffer) >= self.block_size:
                chunk = self.buffer[:self.block_size]
                self.buffer = self.buffer[self.block_size:]
                self.stream.on_next(np.array(chunk).reshape(1, -1))

        except Exception as e:
            print(f"Error processing PCM data: {e}")
            raise

    def finalize(self):
        """
        Finalize the streaming by adding padding at the end and sending any remaining data.
        """
        # Add zero padding at the end if required
        if self.padding_end > 0:
            num_pad_samples = int(np.rint(self.padding_end * self.sample_rate))
            zero_padding = np.zeros(num_pad_samples, dtype=np.float32)
            self.buffer.extend(zero_padding)

        # Send the remaining data if any
        if len(self.buffer) > 0:
            last_chunk = np.array(self.buffer).reshape(1, -1)
            self.stream.on_next(last_chunk)
            self.buffer = []

        # Complete the stream
        self.stream.on_completed()

    def read(self):
        """
        Required by the AudioSource interface, but not used in this implementation.
        """
        pass

    def close(self):
        """
        Closes the audio stream.
        """
        self.stream.on_completed()