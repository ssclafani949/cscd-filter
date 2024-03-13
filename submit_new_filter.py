import csky as cy
import glob, os
from submitter import Submitter
import time
import argparse

p = argparse.ArgumentParser()
p.add_argument('--nfiles', dest='nfiles', type=int)
p.add_argument('--start', dest='start', type=int, default=0)

args = p.parse_args()





def submit_do_cascade_filter (nfiles, start):
    T = time.time ()
    icetray = '/data/user/ssclafani/software/meta-projects/icetray/build/env-shell.sh'
    job_basedir = '/scratch/ssclafani/cascade_filter/'
    job_dir = '{}//T_{:17.6f}'.format (job_basedir, T)
    sub = Submitter (job_dir=job_dir, memory=4, 
        max_jobs=1000, config = 'data_user/cscd-filter/submitter_config')
    commands, labels = [], []
    script = os.path.abspath('pole_to_l3.py')
    exp = glob.glob('/data/exp/IceCube/2024/filtered/PFFilt/*/*')
    gcd_base = '/data/user/ssclafani/cscd-filter/gcd/'
    print(nfiles)
    infiles = sorted(exp)[start:nfiles]
    outbase = '/data/user/ssclafani/cscd-filter/data/'
    for infile in infiles:
        date = infile.split('/')[7]
        infile_name = infile.split('/')[-1]
        runnum = infile_name.split('Run')[1][:8]
        subrun_num = infile_name.split('_')[-1][:8]
        gcd = gcd_base + date + '/PFGCD_Run{}_Subrun00000000.i3.gz'.format(runnum)
        outdir = cy.utils.ensure_dir(outbase + 'Run{}/'.format(runnum))
        outfilen = 'cascade_l3_Run{}_Subrun{}.i3.gz'.format(runnum, subrun_num)
        outfile = outdir + outfilen
        
        fmt = '{} {}  -i {} -g {} -o {} --qify'
        command = fmt.format (icetray, script,  infile, gcd , outfile)
        fmt =  'filter_run_{}_{}'
        label = fmt.format (runnum , subrun_num)
        commands.append (command)
        labels.append (label)
    sub.submit_npx4 (commands, labels)


submit_do_cascade_filter(args.nfiles, args.start)
