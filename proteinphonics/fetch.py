# proteinphonics/fetch.py
import os
import time
import requests
from config import ENSEMBL_REST_SERVER, ENSEMBL_HEADERS_JSON, ENSEMBL_HEADERS_FASTA, FASTA_DIR
from proteinphonics.utils import ensure_directory_exists

def fetch_ensembl_protein_id(gene_name, species):
    """
    Fetch the Ensembl protein ID for a given gene in the specified species.
    """
    ext = f"/lookup/symbol/{species}/{gene_name}?expand=1"
    url = ENSEMBL_REST_SERVER + ext
    response = requests.get(url, headers=ENSEMBL_HEADERS_JSON)
    response.raise_for_status()
    decoded = response.json()
    transcripts = decoded.get('Transcript', [])
    for transcript in transcripts:
        protein_id = transcript.get('Translation', {}).get('id')
        if protein_id:
            return protein_id
    return None

def fetch_ensembl_ortholog_protein_id(reference_gene, reference_species, target_species):
    """
    Fetch the Ensembl protein ID for an ortholog in the target species based on a reference gene.
    """
    ext = f"/homology/symbol/{reference_species}/{reference_gene}?target_species={target_species}&type=orthologues&content-type=application/json"
    url = ENSEMBL_REST_SERVER + ext
    response = requests.get(url, headers=ENSEMBL_HEADERS_JSON)
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
    """
    Fetch the protein sequence in FASTA format for a given protein ID.
    """
    ext = f"/sequence/id/{protein_id}?type=protein"
    url = ENSEMBL_REST_SERVER + ext
    print(f"Fetching protein sequence for ID: {protein_id}")
    response = requests.get(url, headers=ENSEMBL_HEADERS_FASTA)
    if not response.ok:
        response.raise_for_status()
    return response.text

def fetch_sequences(gene_name, species_list, reference_species=None):
    """
    Fetch protein sequences for a given gene across a list of species.
    The resulting sequences are stored in a FASTA file located under FASTA_DIR.
    If the file already exists, fetching is skipped.
    """
    # Ensure the FASTA directory exists
    ensure_directory_exists(FASTA_DIR)
    
    fasta_file = os.path.join(FASTA_DIR, f"{gene_name}.fasta")
    
    if os.path.exists(fasta_file):
        print(f"{fasta_file} already exists, skipping fetch.")
        return fasta_file
    
    if not reference_species:
        reference_species = species_list[0]
    if reference_species not in species_list:
        raise ValueError(f"Reference species '{reference_species}' must be in species_list.")
    
    # Standardize species names for API queries
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
                fasta_lines = fasta_data.strip().split("\n")
                # Replace header with species name for clarity
                fasta_lines[0] = f">{species_query}"
                fasta_entry = "\n".join(fasta_lines)
                print(f"Writing FASTA entry for {species}:\n{fasta_entry}\n")
                fasta_file_obj.write(fasta_entry + "\n")
                fasta_file_obj.flush()
            else:
                print(f"Warning: No sequence found for {gene_name} in {species}.")
            # Pause to avoid hitting rate limits
            time.sleep(0.5)
    
    print(f"FASTA file written to: {fasta_file}")
    return fasta_file
