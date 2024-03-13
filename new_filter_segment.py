#!/usr/bin/env python3
#level3recos.py

import sys, os, glob
from icecube.icetray import I3Tray
from icecube import icetray

from icecube.offline_filterscripts.cascade_filter.CascadeL3TraySegment import CascadeL3

infiles = '/data/user/ssclafani/cscd-filter/data/Run00138812_Subrun00000000_00000000_L1.i3.bz2'
outfile = '/data/user/ssclafani/cscd-filter/data/test_Run00138811_segment.i3.bz2'
gcd = '/data/user/ssclafani/cscd-filter/gcd/0102/PFGCD_Run00138811_Subrun00000000.i3.gz'
name = 'CscdL3'
print('running cscdl3')
icetray.logging.console()   # Make python logging work
icetray.I3Logger.global_logger.set_level(icetray.I3LogLevel.LOG_WARN)

tray = I3Tray()
tray.AddSegment(CascadeL3,
                infiles=infiles,
                gcdfile=gcd,
                output_i3=outfile)


tray.Execute()
