#!/usr/bin/env python3

import os
import json

import logging
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(process)s - %(message)s')

import ppdx
ppdx.config.cread('config-ppdx.ini')

# Setting up parsl for local execution using max of 12 threads
import parsl
from parsl.providers import LocalProvider
from parsl.channels import LocalChannel
from parsl.config import Config
from parsl.executors import HighThroughputExecutor
local_htex = Config(
    executors=[
        HighThroughputExecutor(
            label="htex_Local",
            cores_per_worker=1,
            max_workers=12,
            provider=LocalProvider(
                channel=LocalChannel(),
                init_blocks=1,
                max_blocks=1,
            ),
        )
    ],
    strategy=None,
)
parsl.load(local_htex)

def compute(dbpath, nmodels=12, config='pool:12', protocol='modeller_fast'):

    # Create list of descriptors to compute
    desc = list()
    # Molecular
    #desc += ['TMscore']
    desc += ['HB_BH', 'HB_WN', 'HB_KS']
    desc += ['BSA', 'BSA_C', 'BSA_A', 'BSA_P', 'NIS_P', 'NIS_C', 'NIS_A', 'NRES']
    desc += ['sticky_tot', 'sticky_avg']
    desc += ['IC_TOT', 'IC_AA', 'IC_PP', 'IC_CC', 'IC_AP', 'IC_CP', 'IC_AC']
    # Docking
    #desc += ['ZRANK', 'ZRANK2']
    #desc += ['pyDock', 'pyDock_elec', 'pyDock_vdw', 'pyDock_desolv']
    #desc += ['ATTRACT']
    #desc += ['FireDock', 'FireDock_aVdW', 'FireDock_rVdW', 'FireDock_ACE', 'FireDock_inside',
    #            'FireDock_aElec', 'FireDock_rElec', 'FireDock_laElec', 'FireDock_lrElec',
    #            'FireDock_hb', 'FireDock_piS', 'FireDock_catpiS', 'FireDock_aliph']
    # Statistical Potentials
    desc += ['RF_HA_SRS']
    #desc += ['RF_CB_SRS_OD']
    #desc += ['ipot_aace167', 'ipot_aace18', 'ipot_aace20', 'ipot_rrce20']
    #desc += ['SOAP-PP-Pair', 'SOAP-Protein-OD']
    #desc += ['DOPE', 'DOPE-HR']
    # Implicit Solvents
    #desc += ['AGBNP']
    #desc += ['FACTS_ELEC', 'FACTS_VDW', 'FACTS_GB', 'FACTS_ASP', 'FACTS_POL', 'FACTS_TOT']
    #desc += ['GBMV_ELEC', 'GBMV_VDW', 'GBMV_GB', 'GBMV_ASP', 'GBMV_POL', 'GBMV_TOT']
    #desc += ['GBSW_ELEC', 'GBSW_VDW', 'GBSW_GB', 'GBSW_ASP', 'GBSW_POL', 'GBSW_TOT']
    #desc += ['CDIE_ELEC', 'CDIE_VDW', 'CDIE_TOT']
    #desc += ['RDIE_ELEC', 'RDIE_VDW', 'RDIE_TOT']
    #desc += ['OMM_vacuum', 'OMM_HCT', 'OMM_OBC1', 'OMM_OBC2', 'OMM_GBn', 'OMM_GBn2']
    # Folding
    #desc += ['FoldX', 'FoldX_backbone_hbond', 'FoldX_sidechain_hbond', 'FoldX_vdw', 
    #            'FoldX_elec', 'FoldX_solvation_polar', 'FoldX_solvation_hydrophobic', 
    #            'FoldX_entropy_sidechain', 'FoldX_entropy_mainchain']
    #desc += ['Rosetta_dg', 'Rosetta_sasa', 'Rosetta_hbonds']
    # Entropy
    desc += ['ENM_R6', 'ENM_EXP']
    # Binding
    desc += ['Prodigy_IC_NIS']

    # Prepare list of what to compute
    inputs = list()
#     sequences = ppdx.tools.read_multi_fasta('ppdb/ppdb.seq')
    sequences = ppdx.tools.read_multi_fasta('ppdb/sequences.seq')
    with open('ppdb/ppdb.txt') as fp:
        for line in fp:
            if line[0]=='#':
                continue
            name, recn, lign, dgexp, tpl = line.split()
            sequence = sequences[name]
            template = os.path.join(dbpath, tpl)
            nchains = (int(recn), int(lign))
            #if name.startswith('FY'):
            inputs.append([name, sequence, nchains, template])

    # Compute the descriptors
    ppdx.eval_descriptors(protocol, desc, inputs, nmodels=nmodels, config=config)
    ppdx.save_descriptors_json(inputs, 'descriptors-all.json')


if __name__=='__main__':
    ppdx.WRKDIR = os.path.join(os.getcwd(), "models")
    for n in range(20):
        for protocol in ['modeller_fast', 'modeller_veryfast', 'modeller_slow', 'rosetta']:
            print(n, protocol)
            compute(os.path.join(os.getcwd(), 'ppdb'), nmodels=n+1, config='parsl', protocol=protocol)
            ppdx.clean()
            if os.path.isfile('kill'):
                print('Kill!')
                quit()


