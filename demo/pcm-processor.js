class PCMProcessor extends AudioWorkletProcessor {
  constructor() {
      super();
      this.accumulatedBuffer = new Float32Array(0);
      this.targetBufferLength = sampleRate * 0.5; // Target 0.5 seconds of audio
  }

  process(inputs, outputs, parameters) {
      const input = inputs[0];
      if (input.length > 0) {
          const channelData = input[0]; // Get PCM data from the first channel

          // Accumulate buffers
          const newBuffer = new Float32Array(this.accumulatedBuffer.length + channelData.length);
          newBuffer.set(this.accumulatedBuffer, 0);
          newBuffer.set(channelData, this.accumulatedBuffer.length);
          this.accumulatedBuffer = newBuffer;

          // If the accumulated buffer is at least 0.5 seconds, send it
          if (this.accumulatedBuffer.length >= this.targetBufferLength) {
              const dataToSend = this.accumulatedBuffer.subarray(0, this.targetBufferLength);
              this.port.postMessage(dataToSend); // Send raw PCM data to the main thread

              // Remove the sent data from the accumulated buffer
              this.accumulatedBuffer = this.accumulatedBuffer.subarray(this.targetBufferLength);
          }
      }

      return true; // Return true to keep the processor alive
  }
}

registerProcessor('pcm-processor', PCMProcessor);
