import os, sys, subprocess

import glob
nfiles = 3
base_dir = '/data/user/ssclafani/cscd-filter/'

script = '/data/user/ssclafani/software/meta-projects/icetray/src/offline_filterscripts/python/cascade_filter/example.py'

inputs = glob.glob('/data/exp/IceCube/2024/filtered/PFFilt/0102/*')
gcds =glob.glob('/data/user/ssclafani/cscd-filter/gcd/0102/*')

for i in sorted(inputs)[:nfiles]:
    run = i.split('/')
    run = run[-1].split('_')
    subrun = run[4]
    run = run[2][3:]
    print(run)
    if '138810' in run:
        gcd = None
    elif '138811' in run:
        gcd = gcds[0]
    elif '138812' in run:
        gcd = gcds[1]
    elif '138813' in run:
        gcd = gcds[2]

    outdir = '/data/user/ssclafani/cscd-filter/data'
    outfile = 'newfilter__Run{}_SubRun{}'.format(run, subrun)
    o = os.path.join(outdir, outfile)
    
    if gcd:
        print('Running File: {}'.format(i))
        print('with GCD: {}'.format(gcd))
        print('Output: {}'.format(o))
        subprocess.run('python {} -i {} -g {} -o {} --qify'.format(script, i, gcd, o), shell=True)
    
