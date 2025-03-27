# app.py
import os
import base64
import streamlit as st
from proteinphonics.midi_generation import create_evolutionary_music
from config import MIDIS_DIR, INSTRUMENT_MAP
import components.html_midi_player as html_midi_player  # New html-midi-player component wrapper

# Set page configuration
st.set_page_config(page_title="ProteinPhonics", layout="wide")

st.title("ProteinPhonics: Protein to Music")
st.write("Transform protein sequences into interactive MIDI compositions!")

# Sidebar basic inputs
st.sidebar.header("User Inputs")
gene_name = st.sidebar.text_input("Gene Name", value="MT-CO1")
tempo_bpm = st.sidebar.number_input("Tempo (BPM)", value=120, step=10)
time_step = st.sidebar.number_input("Time Step (seconds)", value=0.1, step=0.1)

# Advanced options inside an expander
with st.sidebar.expander("Advanced: Species & Instrument Options", expanded=False):
    species_options = list(INSTRUMENT_MAP.keys())
    selected_species = st.multiselect("Select Species", options=species_options, default=species_options)
    if selected_species:
        reference_species = st.selectbox("Reference Species", options=selected_species, index=0)
    else:
        reference_species = None

    st.write("### Instrument Mapping")
    instrument_mapping = {}
    for species in selected_species:
        default_instrument = INSTRUMENT_MAP.get(species, 0)
        instrument_mapping[species] = st.number_input(
            f"Instrument (MIDI Program) for {species}",
            min_value=0, max_value=127, value=default_instrument, step=1
        )

if st.button("Generate Music"):
    if not gene_name:
        st.error("Please enter a valid gene name.")
    elif not selected_species:
        st.error("Please select at least one species.")
    else:
        with st.spinner("Processing... This may take a few moments."):
            try:
                midi_filename = os.path.join(MIDIS_DIR, f"{gene_name}.mid")
                create_evolutionary_music(
                    gene_name,
                    selected_species,
                    reference_species,
                    midi_filename=midi_filename,
                    tempo_bpm=tempo_bpm,
                    time_step=time_step,
                    instrument_mapping=instrument_mapping
                )
                st.success("MIDI file generated successfully!")
                
                # Provide a download button for the MIDI file
                with open(midi_filename, "rb") as midi_file:
                    st.download_button("Download MIDI", midi_file, file_name=f"{gene_name}.mid", mime="audio/midi")
                
                # Read and encode the MIDI file as a base64 data URL
                with open(midi_filename, "rb") as f:
                    midi_bytes = f.read()
                midi_base64 = base64.b64encode(midi_bytes).decode("utf-8")
                midi_data_url = f"data:audio/midi;base64,{midi_base64}"
                # midi_data_url = midi_filename  # Use the file path directly
                
                st.write("### Interactive MIDI Player")
                # Call the new html-midi-player component with the data URL
                html_midi_player.st_html_midi_player(midi_file_url=midi_data_url, height=300)
            except Exception as e:
                st.error(f"An error occurred during processing: {e}")
