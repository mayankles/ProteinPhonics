# proteinphonics/alignment.py
import os
import subprocess
from config import MUSCLE_EXECUTABLE, ALIGNMENTS_DIR
from proteinphonics.utils import ensure_directory_exists

def perform_alignment(input_fasta):
    """
    Perform multiple sequence alignment using MUSCLE.
    The aligned sequences are written to a file in ALIGNMENTS_DIR.
    
    Parameters:
        input_fasta (str): Path to the input FASTA file.
        
    Returns:
        output_file (str): Path to the alignment file.
    """
    ensure_directory_exists(ALIGNMENTS_DIR)
    
    # Create an output file name based on the input file name.
    base_name = os.path.basename(input_fasta)
    output_file = os.path.join(ALIGNMENTS_DIR, f"aligned_{base_name}")
    
    # If alignment already exists, skip the alignment step.
    if os.path.exists(output_file):
        print(f"Alignment file {output_file} already exists. Using cached version.")
        return output_file
    
    # Build the MUSCLE command.
    cmd = [MUSCLE_EXECUTABLE, "-in", input_fasta, "-out", output_file]
    print("Running MUSCLE alignment:")
    print(" ".join(cmd))
    
    # Run the command; raises an error if MUSCLE fails.
    # subprocess.run(cmd, check=True)
    
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("MUSCLE stdout:", result.stdout.decode())
    print("MUSCLE stderr:", result.stderr.decode())
    result.check_returncode()  # This will raise an error with the captured logs if MUSCLE fails.

    print(f"Alignment complete. Output written to {output_file}")
    return output_file

def read_alignment(alignment_file, file_format="fasta"):
    """
    Read an alignment file using Biopython's AlignIO.
    
    Parameters:
        alignment_file (str): Path to the alignment file.
        file_format (str): Format of the alignment file (default is "fasta").
        
    Returns:
        alignment: A Biopython alignment object.
    """
    from Bio import AlignIO
    alignment = AlignIO.read(alignment_file, file_format)
    return alignment
