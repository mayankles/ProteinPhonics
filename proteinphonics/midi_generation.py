# proteinphonics/midi_generation.py
import os
import pretty_midi
from proteinphonics.fetch import fetch_sequences
from proteinphonics.alignment import perform_alignment, read_alignment
from config import AA_PITCH_MAP, MIDIS_DIR

def alignment_to_midi(alignment, aa_pitch_map, species_instrument_map, midi_filename, tempo_bpm=120, time_step=0.5):
    """
    Convert the alignment to a MIDI file.
    
    Parameters:
        alignment: A Biopython alignment object.
        aa_pitch_map: Dictionary mapping amino acids to MIDI pitches.
        species_instrument_map: Dictionary mapping species to MIDI program numbers.
        midi_filename (str): Path to save the generated MIDI file.
        tempo_bpm (int): Tempo in beats per minute.
        time_step (float): Duration per note in seconds.
    """
    midi = pretty_midi.PrettyMIDI(initial_tempo=tempo_bpm)
    
    for record in alignment:
        # Convert record ID back to a nicely formatted species name
        species = record.id.replace('_', ' ').title()
        # Get the instrument for this species; default to program 0 (Grand Piano) if not specified
        instrument_program = species_instrument_map.get(species, 0)
        instrument = pretty_midi.Instrument(program=instrument_program, name=species)
        
        # Iterate over the sequence and create notes for non-gap characters.
        for i, aa in enumerate(record.seq):
            if aa == '-':
                continue  # Treat gaps as rests.
            pitch = aa_pitch_map.get(aa, 60)  # Default to middle C if amino acid not mapped.
            note = pretty_midi.Note(velocity=100, pitch=pitch, start=i * time_step, end=(i+1) * time_step)
            instrument.notes.append(note)
        midi.instruments.append(instrument)
    
    midi.write(midi_filename)
    print(f"MIDI file written to: {midi_filename}")

def create_evolutionary_music(gene_name, species_list, reference_species, midi_filename, tempo_bpm=120, time_step=0.5, instrument_mapping=None):
    """
    Orchestrate the pipeline: fetch sequences, perform alignment, and generate a MIDI file.
    
    Parameters:
        gene_name (str): Gene name to process.
        species_list (list): List of species names.
        reference_species (str): Reference species used for fetching orthologs.
        midi_filename (str): Path to save the generated MIDI file.
        tempo_bpm (int): Tempo (beats per minute) for the MIDI file.
        time_step (float): Duration per note in seconds.
        instrument_mapping (dict): Custom mapping from species to MIDI program numbers.
                                   If None, defaults from configuration will be used.
    """
    # Fetch the sequences and write them to a FASTA file.
    fasta_file = fetch_sequences(gene_name, species_list, reference_species)
    
    # Perform sequence alignment using MUSCLE.
    alignment_file = perform_alignment(fasta_file)
    
    # Read the alignment.
    alignment = read_alignment(alignment_file)
    
    # Use provided instrument mapping or fall back to a default from config.
    if instrument_mapping is None:
        from config import INSTRUMENT_MAP
        instrument_mapping = INSTRUMENT_MAP
    
    # Ensure the directory for the MIDI file exists.
    midi_dir = os.path.dirname(midi_filename)
    if not os.path.exists(midi_dir):
        os.makedirs(midi_dir)
    
    # Generate the MIDI file from the alignment.
    alignment_to_midi(alignment, AA_PITCH_MAP, instrument_mapping, midi_filename, tempo_bpm, time_step)
