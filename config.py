# config.py
"""
Configuration settings for ProteinPhonics.
This includes API endpoints, file paths for persistent storage,
database settings, and default mappings.
"""

# Ensembl API configuration
ENSEMBL_REST_SERVER = "https://rest.ensembl.org"
ENSEMBL_HEADERS_JSON = {"Content-Type": "application/json"}
ENSEMBL_HEADERS_FASTA = {"Content-Type": "text/x-fasta"}

# Directory paths for persistent storage
DATA_DIR = "data"
FASTA_DIR = f"{DATA_DIR}/fasta"
ALIGNMENTS_DIR = f"{DATA_DIR}/alignments"
MIDIS_DIR = f"{DATA_DIR}/midis"
AUDIO_DIR = f"{DATA_DIR}/audio"

# Path to the SoundFont file for MIDI to audio conversion
SOUNDFONT_PATH = "soundfonts/FluidR3_GM.sf2"  # Ensure this file exists in the specified location

# Database configuration
DATABASE_URI = "sqlite:///proteinphonics.db"

# MUSCLE executable configuration (MUSCLE should be in your PATH)
MUSCLE_EXECUTABLE = "muscle"

# Amino acid to MIDI pitch mapping
AA_PITCH_MAP = {
    'A': 60, 'V': 61, 'I': 62, 'L': 63, 'M': 64,
    'S': 65, 'T': 66, 'N': 67, 'Q': 68, 'Y': 69,
    'D': 70, 'E': 71, 'K': 72, 'R': 73, 'H': 74,
    'F': 75, 'W': 76, 'C': 77, 'G': 78, 'P': 79,
}

# Species to default instrument mapping (General MIDI program numbers)
INSTRUMENT_MAP = {
    'Homo sapiens': 0,                # Grand Piano
    'Mus musculus': 40,               # Violin
    'Canis lupus familiaris': 24,     # Acoustic Guitar (nylon)
    'Gallus gallus': 68,              # Oboe
    'Xenopus tropicalis': 12,         # Marimba
    'Danio rerio': 11,                # Vibraphone
    'Anolis carolinensis': 73,        # Flute
    'Drosophila melanogaster': 71,    # Clarinet
    'Caenorhabditis elegans': 114,     # Steel Drums
    'Saccharomyces cerevisiae': 21,    # Accordion
}
