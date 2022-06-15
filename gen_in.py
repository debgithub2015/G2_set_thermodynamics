import sys
import os
from ase import Atoms
from ase.collections import g2
from ase.build import molecule
from ase.data import atomic_numbers, atomic_masses
from ase.data.g2_2 import molecule_names as molecule_names_g2_2
from ase.data.g2_2 import atom_names as atom_names_g2_2
ixc=sys.argv[1]

def get_species(chemsym):
        specsym=[]
        for i in range(len(chemsym)):
                newspec=True
                for j in range(len(specsym)):
                        if(chemsym[i]==specsym[j]): newspec=False
                if(newspec): specsym.append(chemsym[i])
        return specsym

def get_pspfile(specname):
        if(specname=='Al'):
               pspfile='al_pbe_v1.uspp.F.UPF'
        elif(specname=='B'):
               pspfile='b_pbe_v1.4.uspp.F.UPF'
        elif(specname=='Be'):
               pspfile='be_pbe_v1.4.uspp.F.UPF'
        elif(specname=='C'):
               pspfile='c_pbe_v1.2.uspp.F.UPF'
        elif(specname=='Cl'):
               pspfile='cl_pbe_v1.4.uspp.F.UPF'
        elif(specname=='F'):
               pspfile='f_pbe_v1.4.uspp.F.UPF'
        elif(specname=='H'):
               pspfile='h_pbe_v1.4.uspp.F.UPF'
        elif(specname=='Li'):
               pspfile='li_pbe_v1.4.uspp.F.UPF'
        elif(specname=='N'):
               pspfile='n_pbe_v1.2.uspp.F.UPF'
        elif(specname=='Na'):
               pspfile='na_pbe_v1.5.uspp.F.UPF'
        elif(specname=='O'):
               pspfile='o_pbe_v1.2.uspp.F.UPF'
        elif(specname=='P'):
               pspfile='p_pbe_v1.5.uspp.F.UPF'
        elif(specname=='S'):
               pspfile='s_pbe_v1.4.uspp.F.UPF'
        elif(specname=='Si'):
               pspfile='si_pbe_v1.uspp.F.UPF'
        else:
               pspfile='%s.pbe-mt_fhi.UPF'%(specname)
        return pspfile

basepath='/deac/thonhauserGrp/chakrad/calculations/database-calc/G2-2_set/'
entry=os.path.join(basepath,'%s')%(ixc)
os.mkdir(entry)
os.chdir(entry)
print(os.getcwd())
for i in range(len(g2)): # range(len(g2)):
   molname=g2.names[i]
   if(not (molname in molecule_names_g2_2 or molname in atom_names_g2_2)): continue
   mol=g2[molname]
   chemsym=mol.get_chemical_symbols()
   spec=get_species(chemsym)
   chempos=molecule(molname).get_positions()
# ADDED by DC
#    posX = chempos[:,0]
#    posY = chempos[:,1]
#    posZ = chempos[:,2]
#    DeltaX = max(posX) - min(posX)
#    DeltaY = max(posY) - min(posY)
#    DeltaZ = max(posZ) - min(posZ)
#    cell = (15+DeltaX,15+DeltaY,DeltaZ+15)
#
#    molecule(molname).center()
#    molecule(molname).set_cell(cell)
 
   entry_1=os.path.join(entry,'%s')%(molname)
   os.mkdir(entry_1)
   os.chdir(entry_1)
   print(os.getcwd())

   finp=open("%s-%s.in"%(molname,ixc),'w')
   finp.write('''&control
   calculation = 'relax'
   restart_mode='from_scratch',
   prefix='%s-%s',
   tstress = .false.
   tprnfor = .true.
   pseudo_dir='/deac/thonhauserGrp/chakrad/calculations/atomandmolecule-qe6.2.1-i2012-C6modif/all_pbe_UPF_v1.5'
   outdir='.'
!   wf_collect = .true.
   verbosity = 'high'
   forc_conv_thr = 2.0d-5
   nstep = 200
/

&system
   ibrav           = 1   ! 1: sc
   celldm(1)       = 30.0
   nat             = %i
   ntyp            = %i
   nspin           = 2
   starting_magnetization = 0.89
   occupations     = 'smearing'
   smearing        = 'gaussian'
   degauss         = 0.002
   ecutwfc         = 50.0
   ecutrho         = 600.0
   input_dft       = '%s'
/

&electrons
   conv_thr        = 1.0d-8
   mixing_beta     = 0.7
   electron_maxstep = 1000
   scf_must_converge = .true.
   diagonalization  = 'cg'
   diago_cg_maxiter= 100
/

&ions
   ion_dynamics = 'bfgs'
/

K_POINTS automatic 
1  1  1  0  0  0

ATOMIC_SPECIES
'''%(molname,ixc,len(chemsym),len(spec),ixc))
   finp.close()
   finp=open("%s-%s.in"%(molname,ixc),'a')
   for j in range(len(spec)):
      finp.write(''' %3s %12.6f %s\n'''%(spec[j],atomic_masses[atomic_numbers[spec[j]]], get_pspfile(spec[j])))
   finp.write('''
ATOMIC_POSITIONS {angstrom}\n''')
   for j in range(len(chemsym)):
      finp.write('''%3s %12.6f %12.6f %12.6f\n'''%(chemsym[j],chempos[j][0],chempos[j][1],chempos[j][2]))

   finp.close()
   fsub=open("submit",'w') 
   fsub.write('''#!/bin/bash
#SBATCH --job-name=%s-%s
#SBATCH --output="%s-%s.o"
#SBATCH --error="%s-%s.e"
#SBATCH --account="thonhauserGrp"
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --cpus-per-task=1
#SBATCH --time=1-00:00:00
#SBATCH --partition="small"
#SBATCH --mem=80Gb
ulimit -u unlimited
module load rhel7/openmpi/4.0.2-intel-2018
mpirun /deac/thonhauserGrp/chakrad/q-e-vdW-DF3/bin/pw.x < "%s-%s.in" > "%s-%s.out"
'''%(molname,ixc,molname,ixc,molname,ixc,molname,ixc,molname,ixc))
   fsub.close
   os.chdir(entry)
   print(os.getcwd())
os.chdir(basepath)
print(os.getcwd())
