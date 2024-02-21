#!/usr/bin/env python3
#level3recos.py

from icecube.icetray import I3Tray
 

import sys, os, glob

from icecube.icetray import I3Tray
from icecube import icetray
#from icecube.filterscripts.offlineL2.Globals import cascade_wg
from icecube.offline_filterscripts.read_superdst_files import read_superdst_files
from icecube.offline_filterscripts.filter_segments.example_filter \
    import example_filter
from icecube.online_filterscripts.base_segments.pole_base_reco_dst import online_basic_recos
from icecube.filterscripts.cascadefilter import CascadeFilter
from icecube.offline_filterscripts.cascade_filter.Cascade_Cuts \
    import tagBranches, cutBranches
from icecube.offline_filterscripts.cascade_filter.HitCleaning_Cascade \
    import CascadeHitCleaning, TopologicalCounter, runVeto_Singles, runVeto_Coinc
from icecube.offline_filterscripts.cascade_filter.Cascade_Recos \
    import OfflineCascadeReco, CascadeLlhVertexFit, preparePulses, HighLevelFits, L3_Monopod,  \
        CascadeLlhVertexFit, TimeSplitFits, CoreRemovalFits
from icecube.offline_filterscripts.cascade_filter.Cascade_Functions \
    import multiCalculator
from icecube.phys_services.which_split import which_split

infiles = '/data/user/ssclafani/cscd-filter/data/new_cscd_filter_prereco.tar.bz2'
outfile = '/data/user/ssclafani/cscd-filter/data/lvl3_Run00138811_recos.i3.bz2'
gcd = '/data/user/ssclafani/cscd-filter/gcd/0102/PFGCD_Run00138811_Subrun00000000.i3.gz'


files = [gcd]

if isinstance(infiles,str):
   files.append(infiles)
else:
   for f in infiles:files.append(f)

AmplitudeTable = "/cvmfs/icecube.opensciencegrid.org/data/photon-tables/splines/ems_mie_z20_a10.abs.fits"
TimingTable = "/cvmfs/icecube.opensciencegrid.org/data/photon-tables/splines/ems_mie_z20_a10.prob.fits"
MCbool = False
MCtype = None
Year = 2024
Minimizer = 'MIGRAD'
split_name = 'InIceSplit'

tray = I3Tray()
tray.AddModule("I3Reader", FilenameList=files)

MCbool = True #simulation                                                                                                    

#now that events have been cut add in former L3 recos

tray.AddSegment(preparePulses, 'newPulses', Simulation=MCbool,
                InIceCscd = which_split('InIceSplit'))

# fitting SPE32/CscdLLH/Bayesian32/Monopod8 for all
tray.AddSegment(HighLevelFits, 'CscdL3_HighLevelFits_IC',
                Pulses='SRTOfflinePulses',
                InIceCscd = which_split('InIceSplit'),
                )

tray.AddSegment(L3_Monopod, 'monopod',
                    Pulses='OfflinePulses',
                    year=2024,
                    AmplitudeTable="/cvmfs/icecube.opensciencegrid.org/data/photon-tables/splines/ems_mie_z20_a10.abs.fits",
                    TimingTable="/cvmfs/icecube.opensciencegrid.org/data/photon-tables/splines/ems_mie_z20_a10.prob.fits",
                    Minimizer = 'MIGRAD'
                    )

tray.AddSegment(TimeSplitFits, 'TimeSplit', Pulses="OfflinePulses")
tray.AddSegment(CoreRemovalFits, 'CoreRemoval', Pulses="OfflinePulses",Vertex="L3_MonopodFit4_AmptFit")
tray.AddModule("I3Writer", "EventWriter", filename=outfile,
               Streams=[icetray.I3Frame.Physics, icetray.I3Frame.DAQ],
               DropOrphanStreams=[icetray.I3Frame.DAQ,
                                          icetray.I3Frame.TrayInfo])


tray.Execute()
