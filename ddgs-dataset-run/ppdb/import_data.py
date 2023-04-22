from pymol import cmd
import pandas as pd
import re
import sys

# Dictionary to convert 1-letter amino acid codes to 3-letter codes
one_to_three_letter = {'A': 'ALA', 'C': 'CYS', 'D': 'ASP', 'E': 'GLU', 'F': 'PHE', 'G': 'GLY', 'H': 'HIS', 'I': 'ILE', 'K': 'LYS', 'L': 'LEU', 'M': 'MET', 'N': 'ASN', 'P': 'PRO', 'Q': 'GLN', 'R': 'ARG', 'S': 'SER', 'T': 'THR', 'V': 'VAL', 'W': 'TRP', 'Y': 'TYR'}

# Load the PDB file
# pdbs_to_load = ["1BJ1", "1C08", "1DQJ", "1DVF", "1JRH", "1KIP", "1KIQ", "1KIR", "1MHP", "1MLC", "1N8Z", "1NCA", "1NMB", "1VFB", "1XGP", "1XGQ", "1XGR", "1XGT", "1XGU", "1YY9", "2B2X", "2BDN", "2NY7", "2NYY", "2NZ9", "3BDY", "3BE1", "3BN9", "3G6D", "3GBN", "3HFM", "3L5X", "3N85", "3NGB", "3SE8", "4FQY", "5C6T"]
pdbs_to_load = ['1DQJ', '1MHP', '1MLC', '1N8Z', '1VFB', '1YY9', '2NY7', '2NYY',
       '3BDY', '3BE1', '3BN9', '3HFM', '3NGB', '1DVF', '1KIQ', '1KIP',
       '1KIR', '1NCA', '1JRH', '1NMB', '3G6D', '1XGU', '1XGP', '1XGQ',
       '1XGR', '1XGT', '3N85', '3L5X', '1BJ1', '2B2X', '2NZ9', '2BDN',
       '5C6T', '3SE8', '1C08', '3GBN', '4FQY']

def import_data():

    # Import data
    data = pd.read_csv("./use_this_data.csv")
    points = data.loc[data["Interface?"] == True]
    # points = points.loc[points["LD"] == 1] # Comment out to do all mutants
    # all_pdbs = points["#PDB"].unique()
    all_pdbs = ['4FQY']
    for pdb in all_pdbs:
        path = f"./{pdb}_all.clean.pdb"
        for mutant in points.loc[points["#PDB"] == pdb]["Mutations"]:
            cmd.load(path)
            muts = re.split(";", mutant)
            for mut in muts:
                mut = re.sub(r"(\w):(\w)(\d+)(\w*)(\w)", r"\1:\2:\3:\5:\4", mut)
                chain, start, pos, muta, ic = re.split(":", mut)
                print(chain, start, pos, muta, ic)
                cmd.wizard("mutagenesis")
                cmd.do("refresh_wizard")
                cmd.get_wizard().set_mode(one_to_three_letter[muta])
                cmd.get_wizard().do_select(f"chain {chain} and resi {pos}{ic}")
                cmd.frame("1")
                cmd.get_wizard().apply()
            
            cmd.set_wizard('done')
            fasta_string = cmd.get_fastastr('all')
            fasta_string = re.findall(r"((?:[ACDEFGHIKLMNPQRSTVWY]{2}[ACDEFGHIKLMNPQRSTVWY]+\n)+)", fasta_string)
            fasta_string = [string.replace("\n", "") for string in fasta_string]
            fasta_string = "/".join(fasta_string)
            fasta_string = f">{pdb}_{mutant}\n{fasta_string}\n\n"
            cmd.delete('all')
            with open("./all_sequences.seq", "a") as fasta_file:
                fasta_file.write(fasta_string)

cmd.extend("import_data", import_data)