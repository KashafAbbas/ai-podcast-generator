# 🎙️ AI Podcast Generator

The **AI Podcast Generator** is a command-line Python tool that automatically generates a short podcast episode on a given topic using LLMs and text-to-speech synthesis. It creates a script in dialogue format (host and guest), generates voice audio using ElevenLabs, and outputs a complete podcast in MP3 format.

---

## 🚀 Features

- Script generation using **GROQ's LLaMA 3** model  
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

<sub>You’ll need the following Python packages: `python-dotenv`, `pydub`, `openai`, `elevenlabs`, and `argparse` (standard library).</sub>

---

## ⚙️ Usage

```bash
python podcast_generator.py --topic "Artificial Intelligence in Education"
```

### Optional Arguments

| Argument               | Description                                | Default        |
|------------------------|--------------------------------------------|----------------|
| `--output_audio_file`  | Output audio filename                      | `podcast.mp3`  |
| `--output_script_file` | Output text script filename                | `script.txt`   |
| `--host_voice`         | Host voice name (e.g. `Aria`)              | `Aria`         |
| `--guest_voice`        | Guest voice name (e.g. `Daniel`)           | `Daniel`       |

---

## 🗣️ Available Voices

You can choose from the following voices:

`Aria`, `Sarah`, `Laura`, `Charlie`, `George`, `Callum`, `River`, `Liam`, `Charlotte`, `Alice`, `Matilda`, `Will`, `Jessica`, `Eric`, `Chris`, `Brian`, `Daniel`, `Lily`, `Bill`

---

## 🧠 How It Works

1. **Generate Script:** Uses the GROQ API to produce a 6-line scripted conversation on the topic (3 lines by the host, 3 by the guest).
2. **Parse Script:** Separates lines for host and guest to maintain conversational flow.
3. **Text-to-Speech:** Converts each line into realistic voice audio using ElevenLabs.
4. **Merge Audio:** Joins the audio lines in dialogue order and saves them as a podcast.

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

## 📌 Example Command

```bash
python podcast_generator.py --topic "Climate Change Solutions" --host_voice "Laura" --guest_voice "Will"
```

---

## 📄 License

This project is for educational/demo purposes only. Make sure to follow the terms of use of GROQ and ElevenLabs when using their APIs.

---
