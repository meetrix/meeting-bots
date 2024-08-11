import numpy as np
import torch
import torchaudio
from os import path

def save_audio(pcm_data, sample_rate=48000, output_file="output.wav"):
    """
    Append raw PCM data to a WAV file.

    Parameters:
    - pcm_data (bytes): The raw PCM audio data.
    - sample_rate (int): The sample rate of the audio data.
    - output_file (str): The file path to append the WAV file.

    Returns:
    - str: A confirmation message of the file save operation.
    """
    try:
        # Log data type and shape
        print("Received PCM data type:", type(pcm_data))
        print("PCM data length:", len(pcm_data))

        # Convert PCM bytes to numpy array
        audio_array = np.frombuffer(pcm_data, dtype=np.float32)
        print("Converted audio array shape:", audio_array.shape)

        # Convert to a regular PyTorch tensor
        audio_tensor = torch.tensor(audio_array).unsqueeze(0)

        # Append the audio data to the WAV file
        with torch.no_grad():
            if not torch.tensor(audio_tensor.shape).prod().item():
                raise ValueError("Received empty audio tensor, nothing to append")

            if not path.exists(output_file):
                # If the file does not exist, save it as a new file
                torchaudio.save(output_file, audio_tensor, sample_rate, format='wav')
                print(f"PCM data saved to new file {output_file}")
            else:
                # If the file exists, load it and concatenate the new data
                existing_audio, _ = torchaudio.load(output_file)
                combined_audio = torch.cat([existing_audio, audio_tensor], dim=1)
                torchaudio.save(output_file, combined_audio, sample_rate, format='wav')
                print(f"PCM data appended to {output_file}")

        return f"PCM data appended to {output_file}"
    
    except Exception as e:
        print(f"Error processing PCM data: {e}")
        raise
