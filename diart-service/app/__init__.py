from diart import SpeakerDiarization
from diart.sources import WebSocketAudioSource
from diart.inference import StreamingInference

def main():
    # Initialize the Speaker Diarization pipeline
    pipeline = SpeakerDiarization()

    # Setup the WebSocket Audio Source
    source = WebSocketAudioSource(pipeline.config.sample_rate, "0.0.0.0", 7007)

    # Create the Streaming Inference instance
    inference = StreamingInference(pipeline, source)

    # Attach hooks to process the output and send to source
    inference.attach_hooks(lambda ann_wav: source.send(ann_wav[0].to_rttm()))

    # Run the prediction
    prediction = inference()

    # For demonstration, print the prediction (if any)
    print(prediction)

if __name__ == "__main__":
    main()
