#!/usr/bin/env python3


import sys, os
from timeit import default_timer as timer
import ppdg
import logging
log = logging.getLogger(__name__)

def rosetta(wrkdir):
    """
        Rosetta
    """
    time_start = timer()
    basepath = os.getcwd()
    os.chdir(wrkdir)
    log.info("Getting Rosetta scoring...")

    # Relax
    with open('rosetta_relax', 'w') as fp:
        fp.write("ramp_repack_min 1 0.1 0.0\n")
        fp.write("accept_to_best\n")
    ret = ppdg.tools.execute("relax.static.linuxgccrelease -s complexAB.pdb -relax:script rosetta_relax -default_max_cycles 200 >rosetta_relax.out 2>&1")
    if ret!=0:
        os.chdir(basepath)
        raise ValueError("Rosetta relax failed!")

    # Score
    ret = ppdg.tools.execute("InterfaceAnalyzer.static.linuxgccrelease -s complexAB_0001.pdb -interface G_HL -pack_input true -out:file:score_only rosetta_score_interface.sc >rosetta_score.out 2>&1")
    if ret!=0:
        os.chdir(basepath)
        raise ValueError("Rosetta score failed!")

    # Parse output
    with open('rosetta_score_interface.sc', 'r') as fp:
        terms = fp.readlines()[-1].split()

    os.chdir(basepath)
    time_end = timer()
    desc = dict()
    desc['Rosetta_dg'] = float(terms[5])
    desc['Rosetta_sasa'] = float(terms[8])
    desc['Rosetta_hbonds'] = float(terms[12])
    desc['>TIME_Rosetta'] = time_end-time_start
    return desc
     
if __name__=='__main__':
    ppdg.readconfig('config-ppdg.ini')
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    print(rosetta(sys.argv[1]))

