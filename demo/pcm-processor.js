class PCMProcessor extends AudioWorkletProcessor {
  constructor() {
    super();
    this._bufferSize = 409600;
    this._buffer = new Float32Array(this._bufferSize);
    this._bytesWritten = 0;
  }

  _isBufferFull() {
    return this._bytesWritten >= this._bufferSize;
  }

  _appendToBuffer(channelData) {
    for (let i = 0; i < channelData.length; i++) {
      if (this._isBufferFull()) {
        this._flush();
      }
      this._buffer[this._bytesWritten++] = channelData[i];
    }
  }

  _flush() {
    // Send the full buffer to the main thread
    this.port.postMessage({
      buffer: this._buffer.slice(0, this._bytesWritten)
    });
    // Reset the buffer
    this._bytesWritten = 0;
  }

  process(inputs, outputs, parameters) {
    const input = inputs[0];
    if (input.length > 0) {
      const channelData = input[0];
      this._appendToBuffer(channelData);
    }
    return true;
  }
}

registerProcessor('pcm-processor', PCMProcessor);
