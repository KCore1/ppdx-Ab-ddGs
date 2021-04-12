#!/usr/bin/env python3

import os, shutil
import ppdg
import logging
log = logging.getLogger(__name__)

def charmify(fname, nsteps=100):

    basepath = os.getcwd()
    wrkdir, name = os.path.split(fname)

    basename = ''.join(name.split('.')[0:-1]) + '-chm'

    if os.path.isfile(os.path.join(wrkdir, basename+'.psf')) and os.path.isfile(os.path.join(wrkdir, basename+'.pdb')):
        #log.info('Charmm outputs already present, recycling data!')
        return
    else:
        log.info("Charmify-ing pdb %s" % (fname))

    os.chdir(wrkdir)

    pdb = ppdg.Pdb(name)
    pdb.fix4charmm()
    pdb.chain2segid()
    pdb.set_occupancy(1.0)
    pdb.set_beta(1.0)
    pdb.remove_hydrogens()

    chains = pdb.split_by_chain()
    nchains = len(chains)
    cmd = ppdg.CHARMM
    cmd += ' nc=%d ' % nchains
    i=1
    for ch, pdb in chains.items():
        pdb.write("chain_%s.pdb" % (ch.lower()))
        cmd += 'c%d=%s ' % (i, ch)
        i += 1
    cmd += 'name=chain_ out=%s ' % (basename)
    cmd += 'nsteps=%d ' % (nsteps)
    cmd += 'ffpath=%s ' % (ppdg.FFPATH)
    cmd += '-i buildgen.inp >%s 2>&1' % (basename+'.out')

    ppdg.link_data('buildgen.inp')
    ppdg.link_data('disu.str')

    ret = ppdg.tools.execute(cmd)
    os.chdir(basepath)
    if ret!=0:
        raise ValueError("Charmm failed while running < %s > in %s" % (cmd, wrkdir))


#def charmm_model(wrkdir, tpl_complex, tpl_receptor, tpl_ligand):

    # Make working directory and cd into it
#    if not os.path.isdir(wrkdir):
#        os.makedirs(wrkdir)
#    basepath = os.getcwd()
#    os.chdir(wrkdir)
#
#    # Chamify!
#    for name, tpl in zip(['complex','receptor','ligand'], [tpl_complex,tpl_receptor,tpl_ligand]):
#        if not os.path.isdir(name):
#            os.makedirs(name)
#        if not os.path.isfile(os.path.join(name, 'model.pdb')):
#            shutil.copy2(tpl, os.path.join(name, 'template.pdb'))
#            charmify(os.path.join(name, 'template.pdb'))
#            os.symlink('template-chm.pdb', os.path.join(name, 'model.pdb'))
#            os.symlink('template-chm.cor', os.path.join(name, 'model.cor'))
#            os.symlink('template-chm.psf', os.path.join(name, 'model.psf'))
#
#    os.chdir(basepath)

