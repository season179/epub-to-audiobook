# Fine-grained Control - Fish Audio

To use fine-grained control, you can use either our SDK, API, or Playground.

SDK/API: We recommend disabling normalization by setting `"normalize": false` in the request body. This ensures that the API doesn’t alter the intonation of control tags.

Playground: You can use V1.6 Control Model, without setting any other options.

## Phoneme Control

Phoneme control allows you to specify exact pronunciations for words or characters. Currently, we support:

*   CMU Arpabet (for English)
*   Pinyin (for Chinese)

To use phoneme control, wrap the desired pronunciation in `<|phoneme_start|>` and `<|phoneme_end|>` tags. Each tag should contain a single word or character.

### English Example

Standard: “I am an engineer.”  
With phoneme control: “I am an `<|phoneme_start|>EH N JH AH N IH R<|phoneme_end|>`.”

### Chinese Example

Standard: “我是一个工程师。“  
With phoneme control: “我是一个`<|phoneme_start|>gong1<|phoneme_end|><|phoneme_start|>cheng2<|phoneme_end|><|phoneme_start|>shi1<|phoneme_end|>`。“

Paralanguage
------------

Paralanguage controls allow you to add natural speech elements and pauses to make the generated speech sound more human-like. There are two main types of controls:

### Pause Words

You can use common pause words like “um”, “uh”, “嗯”, “啊” to control the rhythm of the speech.

### Special Effects

The following special effects can be added using parentheses:

| Effect | Description | First Available | Stage |
| --- | --- | --- | --- |
| `(break)` | Short pause | V1.6 | Experimental |
| `(long-break)` | Extended pause | V1.6 | Experimental |
| `(breath)` | Breathing sound | V1.6 | Experimental |
| `(laugh)` | Laughter sound | V1.6 | Experimental |
| `(cough)` | Coughing sound | V1.6 | Experimental |
| `(lip-smacking)` | Lip smacking sound | V1.6 | Experimental |
| `(sigh)` | Sighing sound | V1.6 | Experimental |

Example: Standard: “I am an engineer.”  
With paralanguage: “I am, um, an (break) engineer.”
