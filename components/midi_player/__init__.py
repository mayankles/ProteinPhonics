# components/midi_player/__init__.py
import streamlit.components.v1 as components
import os

def st_midi_player(midi_file_url, height=300):
    base_dir = os.path.dirname(__file__)
    html_path = os.path.join(base_dir, "midi_player.html")
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    # Replace the alternate placeholder with the actual MIDI file URL.
    if not isinstance(midi_file_url, str) or not midi_file_url.startswith("data:audio/midi;base64,"):
        raise ValueError("Invalid MIDI file URL")
    html_content = html_content.replace("%%MIDI_FILE_URL%%", midi_file_url)
    return components.html(html_content, height=height)
