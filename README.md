# ProteinPhonics

ProteinPhonics is a web application that transforms protein sequence data into interactive MIDI music compositions using biological data. The project integrates sequence fetching from Ensembl, multiple sequence alignment, MIDI generation, and audio playback with a custom Tone.js interface, all wrapped in an interactive Streamlit app.

## Features

- **Sequence Fetching:** Retrieve and cache protein sequences from Ensembl.
- **Sequence Alignment:** Perform multiple sequence alignments using MUSCLE.
- **MIDI Generation:** Convert aligned protein sequences into MIDI files, mapping amino acids to musical notes.
- **Audio Playback:** Convert MIDI to audio and play directly in the browser using a custom Tone.js-based MIDI player.
- **Database Integration:** Use SQLite to cache fetched data and store metadata for future analysis.
- **Docker Support:** Easily deploy the app in a containerized environment.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/ProteinPhonics.git
   cd ProteinPhonics
   ```

2. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **(Optional) Docker Deployment:**
   ```bash
   docker build -t proteinphonics .
   docker run -p 8501:8501 proteinphonics
   ```

## Usage

Start the Streamlit app with:
    ```bash streamlit run app.py
    ```

This launches the ProteinPhonics web application, where you can input gene names, select species and instruments, generate MIDI files, and listen to the audio playback directly in your browser.

## Development

- **Backend Processing:**  
  The `proteinphonics` package contains modules for fetching sequences, performing alignments, generating MIDI files, and converting MIDI to audio.

- **Custom MIDI Player:**  
  The custom component in `components/midi_player` integrates a Tone.js-based MIDI player for interactive audio playback.

- **Database & Caching:**  
  SQLite is used for caching sequence data and storing metadata to prevent redundant API calls.

## Contributing

Contributions are welcome! Please fork the repository and open a pull request with your improvements.

## License

This project is licensed under the MIT License.

## Acknowledgements

- [Ensembl REST API](https://rest.ensembl.org) for biological data.
- [MIDI.js SoundFonts](https://gleitz.github.io/midi-js-soundfonts/) for instrument samples.
- [Tone.js](https://tonejs.github.io/) for MIDI playback and synthesis.
- [Streamlit](https://streamlit.io/) for the interactive web interface.
