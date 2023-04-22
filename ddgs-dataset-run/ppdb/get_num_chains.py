from pymol import cmd
import re

def get_num_chains():

    pdbs_to_load = ["1BJ1_all.clean.pdb", "1C08_all.clean.pdb", "1DQJ_all.clean.pdb", "1DVF_all.clean.pdb", "1JRH_all.clean.pdb", "1KIP_all.clean.pdb", "1KIQ_all.clean.pdb", "1KIR_all.clean.pdb", "1MHP_all.clean.pdb", "1MLC_all.clean.pdb", "1N8Z_all.clean.pdb", "1NCA_all.clean.pdb", "1NMB_all.clean.pdb", "1VFB_all.clean.pdb", "1XGP_all.clean.pdb", "1XGQ_all.clean.pdb", "1XGR_all.clean.pdb", "1XGT_all.clean.pdb", "1XGU_all.clean.pdb", "1YY9_all.clean.pdb", "2B2X_all.clean.pdb", "2BDN_all.clean.pdb", "2NY7_all.clean.pdb", "2NYY_all.clean.pdb", "2NZ9_all.clean.pdb", "3BDY_all.clean.pdb", "3BE1_all.clean.pdb", "3BN9_all.clean.pdb", "3G6D_all.clean.pdb", "3GBN_all.clean.pdb", "3HFM_all.clean.pdb", "3L5X_all.clean.pdb", "3N85_all.clean.pdb", "3NGB_all.clean.pdb", "3SE8_all.clean.pdb", "4FQY_all.clean.pdb", "5C6T_all.clean.pdb"]

    chain_dict = {}

    for pdb in pdbs_to_load:
        pdb_name = re.sub("_all.clean.pdb", "", pdb)
        cmd.load(pdb)
        chain_dict[pdb_name] = len(cmd.get_chains('all'))
        cmd.delete("all")
    
    return chain_dict

cmd.extend("get_num_chains", get_num_chains)