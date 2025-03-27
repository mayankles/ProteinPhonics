import requests
from Bio import AlignIO, SeqIO
import pretty_midi
import numpy as np
import subprocess
import os
import time

# Example amino acid mapping
AA_PITCH_MAP = {'A':60,'V':61,'I':62,'L':63,'M':64,
                'S':65,'T':66,'N':67,'Q':68,'Y':69,
                'D':70,'E':71,'K':72,'R':73,'H':74,
                'F':75,'W':76,'C':77,'G':78,'P':79}

# Expanded Instruments per diverse species
INSTRUMENT_MAP = {
    'Homo sapiens': 0,                # Grand Piano
    'Mus musculus': 40,               # Violin
    'Canis lupus familiaris': 24,      # Acoustic Guitar (nylon)
    'Gallus gallus': 68,              # Oboe
    'Xenopus tropicalis': 12,         # Marimba
    'Danio rerio': 11,                # Vibraphone
    'Anolis carolinensis': 73,        # Flute
    'Drosophila melanogaster': 71,    # Clarinet
    'Caenorhabditis elegans': 114,    # Steel Drums
    'Saccharomyces cerevisiae': 21,   # Accordion
}

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def fetch_ensembl_protein_id(gene_name, species):
    server = "https://rest.ensembl.org"
    ext = f"/lookup/symbol/{species}/{gene_name}?expand=1"
    headers = {"Content-Type": "application/json"}

    response = requests.get(server + ext, headers=headers)
    response.raise_for_status()

    decoded = response.json()
    transcripts = decoded.get('Transcript', [])
    for transcript in transcripts:
        protein_id = transcript.get('Translation', {}).get('id')
        if protein_id:
            return protein_id
    return None

def fetch_ensembl_ortholog_protein_id(reference_gene, reference_species, target_species):
    server = "https://rest.ensembl.org"
    ext = f"/homology/symbol/{reference_species}/{reference_gene}?target_species={target_species}&type=orthologues&content-type=application/json"

    response = requests.get(server + ext)
    response.raise_for_status()

    decoded = response.json()
    data = decoded.get('data', [])
    if data:
        homologies = data[0].get('homologies', [])
        if homologies:
            protein_id = homologies[0]['target'].get('protein_id')
            return protein_id
    return None

def fetch_ensembl_protein_sequence(protein_id):
    server = "https://rest.ensembl.org"
    ext = f"/sequence/id/{protein_id}?type=protein"
    headers = {"Content-Type": "text/x-fasta"}

    print(f"Fetching protein sequence for ID: {protein_id}")

    response = requests.get(server + ext, headers=headers)
    if not response.ok:
        response.raise_for_status()

    return response.text

def fetch_sequences(gene_name, species_list, reference_species=None, data_dir="data"):
    gene_dir = os.path.join(data_dir, gene_name)
    ensure_directory_exists(gene_dir)
    fasta_file = os.path.join(gene_dir, f"{gene_name}.fasta")
    
    if os.path.exists(fasta_file):
        print(f"{fasta_file} already exists, skipping fetch.")
        return fasta_file

    if not reference_species:
        reference_species = species_list[0]
    if reference_species not in species_list:
        raise ValueError(f"Reference species '{reference_species}' must be included in species_list.")

    reference_species_query = reference_species.lower().replace(" ", "_")

    with open(fasta_file, "w") as fasta_file_obj:
        for species in species_list:
            species_query = species.lower().replace(" ", "_")
            if species == reference_species:
                protein_id = fetch_ensembl_protein_id(gene_name, species_query)
            else:
                protein_id = fetch_ensembl_ortholog_protein_id(gene_name, reference_species_query, species_query)
            
            if protein_id:
                fasta_data = fetch_ensembl_protein_sequence(protein_id)
                fasta_lines = fasta_data.strip().split('\n')
                fasta_lines[0] = f">{species_query}"  # Replace header with species name
                fasta_entry = "\n".join(fasta_lines)
                
                # Debugging: Print the fasta entry to ensure it's correct
                print(f"Writing FASTA entry for {species}:\n{fasta_entry}\n")
                
                # Write the fasta entry to the file
                fasta_file_obj.write(fasta_entry + "\n")
                fasta_file_obj.flush()  # Ensure the data is written to the file
            else:
                print(f"Warning: No sequence found for {gene_name} in {species}.")
            
            # Pause for 0.5 seconds to avoid being blacklisted
            time.sleep(0.5)
    
    print(f"FASTA file written to: {fasta_file}")
    return fasta_file

def perform_alignment(input_fasta, data_dir="data"):
    aligned_dir = os.path.dirname(input_fasta)
    output_file = os.path.join(aligned_dir, "aligned.fasta")
    
    if not os.path.exists(output_file):
        cmd = ['muscle', '-align', input_fasta, '-output', output_file]
        print(f"Running MUSCLE for alignment: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)
    
    alignment = AlignIO.read(output_file, "fasta")
    return alignment

def alignment_to_midi(alignment, aa_pitch_map, species_instrument_map, midi_filename="output.mid", tempo_bpm=120, time_step=0.5):
    midi = pretty_midi.PrettyMIDI(initial_tempo=tempo_bpm)
    for record in alignment:
        species = record.id.replace('_', ' ')
        instrument_program = species_instrument_map.get(species, 0)  # Default to piano if species not found
        instrument = pretty_midi.Instrument(program=instrument_program, name=species)

        for i, aa in enumerate(record.seq):
            if aa == '-':
                continue  # Handle gaps as rests
            pitch = aa_pitch_map.get(aa, 60)  # Default middle C
            note = pretty_midi.Note(
                velocity=100, pitch=pitch, start=i * time_step, end=(i+1) * time_step
            )
            instrument.notes.append(note)
        midi.instruments.append(instrument)

    midi.write(midi_filename)

def create_evolutionary_music(gene_name, species_list, reference_species=None, data_dir="data", midi_filename=None, tempo_bpm=120, time_step=0.5):
    fasta_file = fetch_sequences(gene_name, species_list, reference_species, data_dir)
    alignment = perform_alignment(fasta_file, data_dir)
    print(alignment)
    
    if not midi_filename:
        midi_filename = os.path.join(data_dir, gene_name, f"{gene_name}.mid")
    alignment_to_midi(alignment, AA_PITCH_MAP, INSTRUMENT_MAP, midi_filename=midi_filename, tempo_bpm=tempo_bpm, time_step=time_step)

# Example usage
# print("Hello")
# species_list = list(INSTRUMENT_MAP.keys())
# gene_name = "MT-CO1"
# reference_species = "homo_sapiens"
# create_evolutionary_music("MT-CO1", species_list, midi_filename="MT-CO1.mid", tempo_bpm=360, time_step=0.1)