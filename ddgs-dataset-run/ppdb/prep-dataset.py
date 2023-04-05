#!/usr/bin/env python3

import ppdx
from Bio.PDB import PDBParser
from Bio.SeqUtils import seq1

def main():

    # Read sequences and database
    sequences_ag = ppdx.tools.read_multi_fasta('ag-cleaned.seq')
    sequences_ab = ppdx.tools.read_multi_fasta('kallewaard.seq')
    sequences_ab.update(ppdx.tools.read_multi_fasta('corti.seq'))
    
    # Get aa sequences from each pdb in the dataset and append it chainwise to the resulting file.
    pdbparser = PDBParser()

    structure = pdbparser.get_structure(PDB_ID, PDB_file_path)
    chains = {chain.id:seq1(''.join(residue.resname for residue in chain)) for chain in structure.get_chains()}

    # Prepare list of what to compute
    inputs = list()
    with open('ppdb.txt', 'r') as fpin:
        with open('ppdb.seq', 'w') as fpout:
            for line in fpin:
                if line[0]=='#':
                    continue
                name, recn, lign, dgexp, tpl = line.split()
                ab, ag = name.split('__')
                ab = ab.replace('_', '-')
                sequence = sequences_ag[ag] + '/'
                sequence = sequence*3
                sequence = sequence + seq_nt2aa(sequences_ab[ab+'-VH']) + '/' + seq_nt2aa(sequences_ab[ab+'-VK'])
                fpout.write(">%s\n%s\n" % (name, sequence))

main()

