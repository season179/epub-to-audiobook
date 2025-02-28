# Text to Speech - Fish Audio

## Using the Fish Audio SDK

First, make sure you have the Fish Audio SDK installed. You can install it from [GitHub](https://github.com/fishaudio/fish-audio-python) or [PyPI](https://pypi.org/project/fish-audio-sdk/).

## Example Usage

example.py

```python
from fish_audio_sdk import Session, TTSRequest

session = Session("your_api_key")

# Option 1: Using a reference_id
with open("output1.mp3", "wb") as f:
    for chunk in session.tts(TTSRequest(
        reference_id="MODEL_ID_UPLOADED_OR_CHOSEN_FROM_PLAYGROUND",
        text="Hello, world!"
    )):
        f.write(chunk)
```

This example demonstrates the ways to use the Text-to-Speech API:

Using a `reference_id`: This option uses a model that you’ve previously uploaded or chosen from the playground. Replace `"MODEL_ID_UPLOADED_OR_CHOSEN_FROM_PLAYGROUND"` with the actual model ID.

Make sure to replace `"your_api_key"` with your actual API key, and adjust the file paths as needed.

## Raw API Usage

If you prefer to use the raw API instead of the SDK, you can still use the MessagePack API as described below.

Endpoint Details

*   Method: POST
*   URL: [https://api.fish.audio/v1/tts](https://api.fish.audio/v1/tts)
*   Content-Type: application/msgpack

### Example Usage

example.py

```python
from typing import Annotated, AsyncGenerator, Literal

import httpx
import ormsgpack
from pydantic import AfterValidator, BaseModel, conint


class ServeReferenceAudio(BaseModel):
    audio: bytes
    text: str


class ServeTTSRequest(BaseModel):
    text: str
    chunk_length: Annotated[int, conint(ge=100, le=300, strict=True)] = 200
    # Audio format
    format: Literal["wav", "pcm", "mp3"] = "mp3"
    mp3_bitrate: Literal[64, 128, 192] = 128
    # References audios for in-context learning
    references: list[ServeReferenceAudio] = []
    # Reference id
    # For example, if you want use https://fish.audio/m/7f92f8afb8ec43bf81429cc1c9199cb1/
    # Just pass 7f92f8afb8ec43bf81429cc1c9199cb1
    reference_id: str | None = None
    # Normalize text for en & zh, this increase stability for numbers
    normalize: bool = True
    # Balance mode will reduce latency to 300ms, but may decrease stability
    latency: Literal["normal", "balanced"] = "normal"


request = ServeTTSRequest(
    text="Hello, world!",
    references=[
        ServeReferenceAudio(
            audio=open("lengyue.wav", "rb").read(),
            text="Text in reference AUDIO",
        )
    ],
)

with (
    httpx.Client() as client,
    open("hello.mp3", "wb") as f,
):
    with client.stream(
        "POST",
        "https://api.fish.audio/v1/tts",
        content=ormsgpack.packb(request, option=ormsgpack.OPT_SERIALIZE_PYDANTIC),
        headers={
            "authorization": "Bearer YOUR_API_KEY",
            "content-type": "application/msgpack",
        },
        timeout=None,
    ) as response:
        for chunk in response.iter_bytes():
            f.write(chunk)
```
