#!/usr/bin/env python3

import time
from argparse import ArgumentParser

from icecube.icetray import I3Tray
from icecube import icetray
from icecube.filterscripts.offlineL2.Globals import cascade_wg
from icecube.offline_filterscripts.read_superdst_files import read_superdst_files
from icecube.offline_filterscripts.filter_segments.example_filter \
    import example_filter
from icecube.online_filterscripts.base_segments.pole_base_reco_dst import online_basic_recos
from icecube.filterscripts.cascadefilter import CascadeFilter
from icecube.filterscripts.offlineL2.level2_HitCleaning_Cascade import CascadeHitCleaning
from icecube.filterscripts.offlineL2.level2_Reconstruction_Cascade import OfflineCascadeReco
from icecube.phys_services.which_split import which_split
from icecube.level3_filter_cascade.CascadeL3TraySegment import CascadeL3

from icecube.level3_filter_cascade.level3_Globals import label


start_time = time.asctime()
print('Started:', start_time)


# handling of command line arguments
parser = ArgumentParser(
    prog='UnpackDST',
    description='Stand alone example to simulate pole filtering')
parser.add_argument("-i", "--input", action="store", default=None,
                    dest="INPUT", help="Input i3 file to process", required=True)
parser.add_argument("-o", "--output", action="store", default=None,
                    dest="OUTPUT", help="Output i3 file", required=True)
parser.add_argument("-g", "--gcd", action="store", default=None,
                    dest="GCD", help="GCD file for input i3 file", required=True)
parser.add_argument("--qify", action="store_true", default=False, dest="QIFY",
                    help="Apply QConverter, use if input file is only P frames")
parser.add_argument("-p", "--prettyprint", action="store_true",
                    dest="PRETTY", help="Do nothing other than big tray dump")
args = parser.parse_args()

# Prep the logging hounds.
icetray.logging.console()   # Make python logging work
icetray.I3Logger.global_logger.set_level(icetray.I3LogLevel.LOG_WARN)

tray = I3Tray()

print('Processing: ', args.GCD, args.INPUT)
tray.Add(read_superdst_files, 'read_dst',
         input_files=[args.INPUT],
         input_gcd=args.GCD,
         qify_input=args.QIFY)
# As a stand in for other processing, rerun the basic reconstructions from pole.
tray.Add(online_basic_recos, 'polereco_dst')
# And apply a simple example filter using these simple recos


# lvl2 cascade hit cleaning #
tray.AddSegment(CascadeHitCleaning,'CascadeHitCleaning', 
    If=which_split(split_name='InIceSplit') & (lambda f: cascade_wg(f)),
)
#cascade lvl1 filter
tray.AddSegment(CascadeFilter, "CascadeFilter",
                pulses='CleanedInIcePulses')

# cascade lvl2 reco #
tray.AddSegment(OfflineCascadeReco,'CascadeL2Reco',
    SRTPulses='',
    Pulses='SplitInIcePulses',
    TopoPulses = '',
    If=which_split(split_name='InIceSplit') & (lambda f: cascade_wg(f)),
    suffix='_L2'
)

#tray.AddModule(label,'label_CascadeL2Stream',year=2014)
#selects cascade L2 stream w/o removing IceTop p-frames.
#tray.AddModule(lambda frame: frame['CscdL2'].value and which_split(frame, split_name='InIceSplit'),'SelectCscdL2')
                    
#cascade lvl3 

#tray.AddSegment(CascadeL3,
#                    gcdfile=None,
#                    infiles=None,
#                    output_i3=None,
#                    AmplitudeTable="/cvmfs/icecube.opensciencegrid.org/data/photon-tables/splines/ems_mie_z20_a10.abs.fits",
#                    TimingTable="/cvmfs/icecube.opensciencegrid.org/data/photon-tables/splines/ems_mie_z20_a10.prob.fits",
#                    MCbool=False,
#                    MCtype=None,
#		    Year=2024)

# WG classifiers and filters go here.  All in a single
#  segment with reco and selection

my_garbage = ['QTriggerHierarchy'
              ]
tray.Add("Delete", "final_cleanup",
         keys=my_garbage)

# Write the physics and DAQ frames
tray.AddModule("I3Writer", "EventWriter", filename=args.OUTPUT,
               Streams=[icetray.I3Frame.Physics, icetray.I3Frame.DAQ],
               DropOrphanStreams=[icetray.I3Frame.DAQ,
                                          icetray.I3Frame.TrayInfo])

if args.PRETTY:
    print(tray)
    exit(0)

tray.Execute(100)
#tray.Execute()

tray.PrintUsage(fraction=1.0)
for entry in tray.Usage():
    print(entry.key(), ':', entry.data().usertime)

stop_time = time.asctime()
print('Started:', start_time)
print('Ended:', stop_time)
