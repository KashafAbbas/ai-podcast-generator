# 🎙️ AI Podcast Generator

The **AI Podcast Generator** is a Python tool that automatically generates a podcast episode on a given topic using LLMs and text-to-speech synthesis. It creates a script in dialogue format (host and guest), generates voice audio using ElevenLabs, and outputs a complete podcast in MP3 format.

---

## 🚀 Features

- Script generation using **GROQ's LLaMA 3** model via API
- Realistic voice synthesis with **ElevenLabs API**
- Support for multiple predefined voice options
- Outputs both:
  - A podcast script (`.txt`)
  - A podcast audio file (`.mp3`)

---

## 🧰 Requirements

- Python 3.8+
- `.env` file with the following keys:
  - `GROQ_API_KEY`
  - `ELEVENLABS_API_KEY`

### Install Dependencies

```bash
pip install -r requirements.txt
```

<sub>Required Python packages: `python-dotenv`, `pydub`, `openai`, `elevenlabs`, and `fastapi` + `uvicorn` for the API.</sub>

---

## ⚙️ Usage

### Run from CLI

```bash
python podcast_generator.py --topic "Artificial Intelligence in Education"
```

### Run as API

Start the FastAPI server:

```bash
uvicorn main_api:app --reload
```

Send a `POST` request using any API client (e.g. Postman or browser extension) to:

```
http://127.0.0.1:8000/generate
```

With the JSON body:

```json
{
  "topic": "Future of Renewable Energy",
  "host_voice": "Sarah",
  "guest_voice": "George",
  "output_script_file": "renewable_script.txt",
  "output_audio_file": "renewable_podcast.mp3"
}
```

---

## 🔄 API Endpoint

### `/generate` (POST)

Generate a podcast from a topic and selected voices.

#### Request Body

| Field               | Type   | Required | Description                       |
|--------------------|--------|----------|-----------------------------------|
| `topic`            | string | ✅        | Topic of the podcast              |
| `host_voice`       | string | ❌        | Voice name for the host (default: Aria) |
| `guest_voice`      | string | ❌        | Voice name for the guest (default: Daniel) |
| `output_script_file` | string | ❌        | Output text file name (default: script.txt) |
| `output_audio_file`  | string | ❌        | Output mp3 file name (default: podcast.mp3) |

---

## 🗣️ Available Voices

You can choose from the following voices:

`Aria`, `Sarah`, `Laura`, `Charlie`, `George`, `Callum`, `River`, `Liam`, `Charlotte`, `Alice`, `Matilda`, `Will`, `Jessica`, `Eric`, `Chris`, `Brian`, `Daniel`, `Lily`, `Bill`

---

## 🧠 How It Works

1. **Generate Script:** Uses the GROQ API to produce a 6-line scripted conversation on the topic (3 lines by the host, 3 by the guest).
2. **Parse Script:** Separates lines for host and guest to maintain dialogue.
3. **Text-to-Speech:** Converts each line into realistic voice audio using ElevenLabs.
4. **Merge Audio:** Joins the audio clips in conversation order and saves them as a podcast.

---

## 🔐 .env Configuration

Create a `.env` file in the project root and add:

```env
GROQ_API_KEY=your_groq_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
```

---

## 📁 Output

- `script.txt`: The generated script.
- `podcast.mp3`: The merged audio file containing the full dialogue.

---

## 📌 Example CLI Command

```bash
python podcast_generator.py --topic "Climate Change Solutions" --host_voice "Laura" --guest_voice "Will"
```

---

## 📄 License

This project is for educational/demo purposes only. Make sure to follow the terms of use of GROQ and ElevenLabs when using their APIs.

---
