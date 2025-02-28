# Text to Speech (WebSocket) - Fish Audio

Use two-way websocket to get real-time TTS audio

## Using the Fish Audio SDK

First, make sure you have the Fish Audio SDK installed. You can install it from [GitHub](https://github.com/fishaudio/fish-audio-python) or [PyPI](https://pypi.org/project/fish-audio-sdk/).

## Example Usage

sync.py
```python
from fish_audio_sdk import WebSocketSession, TTSRequest, ReferenceAudio

sync_websocket = WebSocketSession("your_api_key")

def stream():
    text = "Well, you know, machine learning is like, um, this really fascinating field that's basically teaching computers to, eh, figure things out on their own."
    for line in text.split():
        yield line + " "

tts_request = TTSRequest(
    text="",  # Initial text or empty string
    reference_id="MODEL_ID_UPLOADED_OR_CHOSEN_FROM_PLAYGROUND"
)

with open("output.mp3", "wb") as f:
    for chunk in sync_websocket.tts(
        tts_request,
        stream() # Stream the text
    ):
        f.write(chunk)

```

async.py

```python
from fish_audio_sdk import AsyncWebSocketSession, TTSRequest, ReferenceAudio

async_websocket = AsyncWebSocketSession("your_api_key")

async def stream():
    text = "Well, you know, machine learning is like, um, this really fascinating field that's basically teaching computers to, eh, figure things out on their own."
    for line in text.split():
        yield line + " "

tts_request = TTSRequest(
    text="",  # Initial text or empty string
    reference_id="MODEL_ID_UPLOADED_OR_CHOSEN_FROM_PLAYGROUND"
)

with open("output.mp3", "wb") as f:
    async for chunk in async_websocket.tts(
        tts_request,
        stream() # Stream the text
    ):
        f.write(chunk)

```

This example demonstrates the ways to use the Text-to-Speech API with web socket:

Using a `reference_id`: This option uses a model that you’ve previously uploaded or chosen from the playground. Replace `"MODEL_ID_UPLOADED_OR_CHOSEN_FROM_PLAYGROUND"` with the actual model ID.

Make sure to replace `"your_api_key"` with your actual API key, and adjust the file paths as needed.

## Raw WebSocket API Usage

The WebSocket API provides real-time, bidirectional communication for Text-to-Speech streaming. Here’s how the protocol works:

### WebSocket Protocol

1.  **Connection Endpoint**:
    
    *   URL: `wss://api.fish.audio/v1/tts/live`
2.  **Events**:
    
    a. `start` - Initializes the TTS session:
    
    ```json
    {
      "event": "start",
      "request": {
        "text": "",  // Initial empty text
        "latency": "normal",  // "normal" or "balanced"
        "format": "opus",  // "opus", "mp3", or "wav"
        // Optional: Use prosody to control speech speed and volume
        "prosody": {
          "speed": 1.0,  // Speech speed (0.5-2.0)
          "volume": 0    // Volume adjustment in dB
        },
        "reference_id": "MODEL_ID_UPLOADED_OR_CHOSEN_FROM_PLAYGROUND"
        // Optional: Use reference audio instead of reference_id
        "references": [{
          "audio": "<binary_audio_data>",
          "text": "Reference text for the audio"
        }],
      }
    }
    ```
    
    b. `text` - Sends text chunks:
    
    ```json
    {
      "event": "text",
      "text": "Hello world " // Don't forget the space since all text is concatenated
    }
    ```
    
    There is a text buffer on the server side. Only when this buffer reaches a certain size will an audio event be generated.
    
    Sending a stop event will force the buffer to be flushed, return an audio event, and end the session.
    
    c. `audio` - Receives audio data (server response):
    
    ```json
    {
      "event": "audio",
      "audio": "<binary_audio_data>",
      "time": 3.012 // Time taken in milliseconds
    }
    ```
    
    d. `stop` - Ends the session:
    
    ```json
    {
      "event": "stop"
    }
    ```
    
    e. `flush` - Flushes the text buffer: This immediately generates the audio and returns it, if text is too short, it may lead to under-quality audio.
    
    ```json
    {
      "event": "flush"
    }
    ```
    
    f. `finish` - Ends the session (server side):
    
    ```json
    {
      "event": "finish",
      "reason": "stop" // or "error"
    }
    ```
    
    g. `log` - Logs messages from the server if debug is true:
    
    ```json
    {
      "event": "log",
      "message": "Log message from server"
    }
    ```
    
3.  **Message Format**: All messages use MessagePack encoding
    

### Example Usage with OpenAI + MPV

websocket\_example.py

```python
import asyncio
import websockets
import ormsgpack
import subprocess
import shutil
from openai import AsyncOpenAI

aclient = AsyncOpenAI()


def is_installed(lib_name):
    """Check if a system command is available"""
    return shutil.which(lib_name) is not None


async def stream_audio(audio_stream):
    """
    Stream audio data using mpv player
    Args:
        audio_stream: Async iterator yielding audio chunks
    """
    if not is_installed("mpv"):
        raise ValueError(
            "mpv not found, necessary to stream audio. "
            "Install instructions: https://mpv.io/installation/"
        )

    # Initialize mpv process for real-time audio playback
    mpv_process = subprocess.Popen(
        ["mpv", "--no-cache", "--no-terminal", "--", "fd://0"],
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    async for chunk in audio_stream:
        if chunk:
            mpv_process.stdin.write(chunk)
            mpv_process.stdin.flush()

    if mpv_process.stdin:
        mpv_process.stdin.close()
    mpv_process.wait()


async def text_to_speech_stream(text_iterator):
    """
    Stream text to speech using WebSocket API
    Args:
        text_iterator: Async iterator yielding text chunks
    """
    uri = "wss://api.fish.audio/v1/tts/live"  # Updated URI

    async with websockets.connect(
        uri, extra_headers={"Authorization": f"Bearer YOUR_API_KEY"}
    ) as websocket:
        # Send initial configuration
        await websocket.send(
            ormsgpack.packb(
                {
                    "event": "start",
                    "request": {
                        "text": "",
                        "latency": "normal",
                        "format": "opus",
                        "reference_id": "MODEL_ID_UPLOADED_OR_CHOSEN_FROM_PLAYGROUND",
                    },
                    "debug": True,  # Added debug flag
                }
            )
        )

        # Handle incoming audio data
        async def listen():
            while True:
                try:
                    message = await websocket.recv()
                    data = ormsgpack.unpackb(message)
                    if data["event"] == "audio":
                        yield data["audio"]
                except websockets.exceptions.ConnectionClosed:
                    break

        # Start audio streaming task
        listen_task = asyncio.create_task(stream_audio(listen()))

        # Stream text chunks
        async for text in text_iterator:
            if text:
                await websocket.send(ormsgpack.packb({"event": "text", "text": text}))

        # Send stop signal
        await websocket.send(ormsgpack.packb({"event": "stop"}))
        await listen_task


async def chat_completion(query):
    """Retrieve text from OpenAI and pass it to the text-to-speech function."""
    response = await aclient.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": query}],
        max_completion_tokens=512,
        temperature=1,
        stream=True,
    )

    async def text_iterator():
        async for chunk in response:
            delta = chunk.choices[0].delta
            yield delta.content

    await text_to_speech_stream(text_iterator())  # Updated function name


# Main execution
if __name__ == "__main__":
    user_query = "Hello, tell me a very short story, including filler words, don't use * or #."
    asyncio.run(chat_completion(user_query))
```

This example demonstrates:

1.  Real-time text streaming with WebSocket connection
2.  Handling audio chunks as they arrive
3.  Using MPV player for real-time audio playback
4.  Reference audio support for voice cloning
5.  Proper connection handling and cleanup

Make sure to install required dependencies:

```bash
pip install websockets ormsgpack openai
```

And install MPV player for audio playback (optional):

*   Linux: `apt-get install mpv`
*   macOS: `brew install mpv`
*   Windows: Download from [mpv.io](https://mpv.io/)
