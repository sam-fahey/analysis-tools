#!/usr/bin/env python

import ephem, math, sys
import numpy as np
from datetime import datetime

def observer( longitude, latitude, elevation ):
    obs = ephem.Observer()
    obs.lon = longitude
    obs.lat = latitude
    obs.elevation = elevation
    return obs

def sources( ra, dec, time ):
    if not hasattr(ra, '__len__'): ra = [ra]
    if not hasattr(dec, '__len__'): dec = [dec]
    if type(time) == type(datetime(2010,1,1,0,0,0)): time = [time]
    else:
        print "Error: sources() input 'time' must be a datetime object."
        sys.exit()
    if not len(ra) == len(dec) and len(ra) == len(time):
        print "Error: numbers of source parameters are inconsistent!"
        sys.exit()

    src = {}
    src['ra'] = np.array(ra, dtype=float)
    src['dec'] = np.array(dec, dtype=float)
    src['t'] = np.array(time, dtype=datetime)
    return src

def topo_correction( detector_obs, followup_obs, sources ):
    """ Return time adjustment for signal transit at follow-up observatory
    :type   detector_obs: ephem.Observer()
    :param  detector_obs: observatory which detected the sources
    
    :type   followup_obs: ephem.Observer()
    :param  followup_obs: observatory which is looking for simultaneous archived detection (IceCube)
    
    :type   detector_obs: sources() object, defined above
    :param  detector_obs: sources (e.g. FRBs) detected by detector_obs
    """
    
    time_diffs = np.zeros(len(sources['ra']))
    for j in range(len(sources['ra'])):
        ra = sources['ra'][j]
        dec = sources['dec'][j]
        t = sources['t'][j]

        detector_obs.date = ephem.Date(t)
        followup_obs.date = ephem.Date(t)

        detector_separation = ephem.separation( detector_obs.radec_of(0., np.pi/2), [ra, dec] )
        followup_separation = ephem.separation( followup_obs.radec_of(0., np.pi/2), [ra, dec] )

        detector_core_transit = (detector_obs.elevation + 6.317e6) * math.cos( detector_separation )
        followup_core_transit = (followup_obs.elevation + 6.317e6) * math.cos( followup_separation )

        time_diff = ( detector_core_transit - followup_core_transit ) / 3.e8
        time_diffs[j] = time_diff

    return time_diffs

def run_example():

    icecube = observer( np.radians(0.), np.radians(-90.), 2835 )
    arecibo = observer( np.radians(66. + 45./60 + 10./3600)*-1., np.radians(18. + 20./60 + 39./3600), 497 )
    frb121102 = sources( (5. + 32./60)/24 * 2*np.pi, np.radians(33. + 8./60), datetime(2012, 11, 02, 06, 47, 17) )

    print topo_correction( arecibo, icecube, frb121102 )
    # output: [0.03177779]
    # signal expected to traverse IceCube (followup) 31.78 ms after Arecibo (detector) detection of source.

    return None

    
