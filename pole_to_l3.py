#!/usr/bin/env python
import time
from argparse import ArgumentParser

from icecube.icetray import I3Tray
from icecube import icetray
from icecube.offline_filterscripts.read_superdst_files import read_superdst_files
from icecube.offline_filterscripts.filter_segments.example_filter \
    import example_filter
from icecube.online_filterscripts.base_segments.pole_base_reco_dst import online_basic_recos
from icecube.filterscripts.cascadefilter import CascadeFilter
from icecube.phys_services.which_split import which_split
from icecube.offline_filterscripts.cascade_filter.CascadeL3TraySegment import CascadeL3

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
parser.add_argument("--sim", dest="sim", action="store_true", default=True )
args = parser.parse_args()

# Prep the logging hounds.
icetray.logging.console()   # Make python logging work
icetray.I3Logger.global_logger.set_level(icetray.I3LogLevel.LOG_WARN)

tray = I3Tray()
mcBool = args.sim
print('Processing: ', args.GCD, args.INPUT)
tray.Add(read_superdst_files, 'read_dst',
         input_files=[args.INPUT],
         input_gcd=args.GCD,
         qify_input=args.QIFY)

# As a stand in for other processing, rerun the basic reconstructions from pole.
tray.Add(online_basic_recos, 'polereco_dst')
# And apply a simple example filter using these simple recos

#cascade lvl1 filter
tray.AddSegment(CascadeFilter, "CascadeFilter",
                pulses='CleanedInIcePulses',
                If=which_split('InIceSplit'))

#Write the physics and DAQ frames
tray.AddSegment(CascadeL3,
                infiles=None,    
                gcdfile=None,
                output_i3=None)


tray.AddModule("I3Writer", "EventWriter", filename=args.OUTPUT,
               Streams=[icetray.I3Frame.Physics, icetray.I3Frame.DAQ],
               DropOrphanStreams=[icetray.I3Frame.DAQ,
                                          icetray.I3Frame.TrayInfo])
tray.Execute()
