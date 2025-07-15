import os
import argparse
from dotenv import load_dotenv
from pydub import AudioSegment
from openai import OpenAI
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs


# ----------------------------
# 1. CLI Argument Parsing
# ----------------------------
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", required=True)
    parser.add_argument("--output_audio_file", default="podcast.mp3")
    parser.add_argument("--output_script_file", default="script.txt")
    parser.add_argument("--host_voice", default="Aria")
    parser.add_argument("--guest_voice", default="Daniel")
    return parser.parse_args()


# ----------------------------
# 2. Generate Script using Grok
# ----------------------------
def generate_script_with_groq(topic):
    client = OpenAI(
        api_key=os.getenv("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1"
    )

    prompt = (
    f"You are writing a podcast script on the topic: '{topic}'.\n"
    "The script must contain exactly 6 lines — 3 from the HOST and 3 from the GUEST — strictly in this order:\n"
    "HOST: line\n"
    "GUEST: line\n"
    "HOST: line\n"
    "GUEST: line\n"
    "HOST: line\n"
    "GUEST: line\n\n"
    "In the FIRST HOST line, briefly introduce the podcast, host, guest, and topic, and ask the first question in the same sentence.\n"
    "Each HOST line must ask a clear and relevant question.\n"
    "Each GUEST line must directly and insightfully answer the preceding HOST question.\n"
    "Keep each line under 250 characters.\n"
    "Do NOT add any lines beyond this format, and do NOT include summaries or sign-offs."
)


    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=500
    )

    return response.choices[0].message.content


# ----------------------------
# 3. Parse Script
# ----------------------------
def parse_script(script_text):
    host_lines = []
    guest_lines = []

    for line in script_text.splitlines():
        line = line.strip()
        if line.startswith("HOST:") and len(host_lines) < 3:
            host_lines.append(line[5:].strip())
        elif line.startswith("GUEST:") and len(guest_lines) < 3:
            guest_lines.append(line[6:].strip())
        if len(host_lines) == 3 and len(guest_lines) == 3:
            break

    if len(host_lines) != 3 or len(guest_lines) != 3:
        raise ValueError("Script must contain exactly 3 lines for HOST and 3 lines for GUEST.")

    # Interleave lines to preserve dialogue order (HOST → GUEST → HOST → GUEST ...)
    dialogue = []
    for h, g in zip(host_lines, guest_lines):
        dialogue.append(("host", h))
        dialogue.append(("guest", g))

    return dialogue



# ----------------------------
# 4. Convert Text to Audio
# ----------------------------
def convert_text_to_audio(text, voice_id, filename):
    client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

    audio_stream = client.text_to_speech.convert(
        voice_id=voice_id,
        model_id="eleven_monolingual_v1",
        text=text,
        voice_settings=VoiceSettings(stability=0.5, similarity_boost=0.75)
    )

    with open(filename, "wb") as f:
        for chunk in audio_stream:
            f.write(chunk)


# ----------------------------
# 5. Merge Audio Files
# ----------------------------
def merge_audio_files(filenames, output_file):
    final = AudioSegment.empty()
    for file in filenames:
        final += AudioSegment.from_file(file)
    final.export(output_file, format="mp3")


# ----------------------------
# 6. Validate API Keys
# ----------------------------
def validate_env():
    if not os.getenv("GROQ_API_KEY"):
        raise EnvironmentError("GROQ_API_KEY is missing. Please check your .env file.")
    if not os.getenv("ELEVENLABS_API_KEY"):
        raise EnvironmentError("ELEVENLABS_API_KEY is missing. Please check your .env file.")


# ----------------------------
# 7. Main Function
# ----------------------------
def main():
    print("Starting AI Podcast Generation...")

    load_dotenv()
    validate_env()

    args = get_args()

    # Voice name → voice_id mapping
    voice_map = {
        "Aria": "9BWtsMINqrJLrRacOk9x",
        "Sarah": "EXAVITQu4vr4xnSDxMaL",
        "Laura": "FGY2WhTYpPnrIDTdsKH5",
        "Charlie": "IKne3meq5aSn9XLyUdCD",
        "George": "JBFqnCBsd6RMkjVDRZzb",
        "Callum": "N2lVS1w4EtoT3dr4eOWO",
        "River": "SAz9YHcvj6GT2YYXdXww",
        "Liam": "TX3LPaxmHKxFdv7VOQHJ",
        "Charlotte": "XB0fDUnXU5powFXDhCwa",
        "Alice": "Xb7hH8MSUJpSbSDYk0k2",
        "Matilda": "XrExE9yKIg1WjnnlVkGX",
        "Will": "bIHbv24MWmeRgasZH58o",
        "Jessica": "cgSgspJ2msm6clMCkdW9",
        "Eric": "cjVigY5qzO86Huf0OWal",
        "Chris": "iP95p4xoKVk53GoZ742B",
        "Brian": "nPczCjzI2devNBz1zQrb",
        "Daniel": "onwK4e9ZLuTAKqWW03F9",
        "Lily": "pFZP5JQG7iQjIQuC4Bku",
        "Bill": "pqHfZKP75CvOlQylNhV4"
    }

    # Resolve to voice_id
    host_voice_id = voice_map.get(args.host_voice, args.host_voice)
    guest_voice_id = voice_map.get(args.guest_voice, args.guest_voice)

    print("🎙️ Generating script using Groq...")
    raw_script = generate_script_with_groq(args.topic)

    print("📝 Saving script...")
    with open(args.output_script_file, "w") as f:
        f.write(raw_script)

    print("📄 Raw script output:\n", raw_script)

    print("📖 Parsing script...")
    dialogue = parse_script(raw_script)

    print("🔊 Generating audio...")
    audio_files = []
    for i, (speaker, text) in enumerate(dialogue):
        filename = f"line{i + 1}.mp3"
        voice_id = host_voice_id if speaker == "host" else guest_voice_id
        convert_text_to_audio(text, voice_id, filename)
        audio_files.append(filename)

    print("🎧 Merging audio...")
    merge_audio_files(audio_files, args.output_audio_file)

    print(f"✅ Podcast saved to {args.output_audio_file}")


# ----------------------------
# 8. Entry Point
# ----------------------------
if __name__ == "__main__":
    main()
