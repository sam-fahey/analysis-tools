#!/usr/bin/env python

import ephem
import numpy as np
import math

import icecube
from icecube import grbllh, umdtools
from icecube.umdtools import cache
import bg_src_North, bg_src_South
from bg_src_North import Bg_srcs as srcs_north
from bg_src_South import Bg_srcs as srcs_south

srcs_north = srcs_north()
srcs_south = srcs_south()

dec = np.append(srcs_north.zenith, srcs_south.zenith)-np.pi/2
ra = np.append(srcs_north.azimuth, srcs_south.azimuth)
t_obs = np.append(srcs_north.t, srcs_south.t)

print "\n Begin barycentering... \n \n"

arecibo_lat = np.radians(18. + 20./60 + 39./3600) # North: 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13
arecibo_lon = -1*np.radians(66. + 45./60 + 10./3600)
arecibo_D_to_IC = 1.622 # in Earth radii
gbt_lat = np.radians(38. + 25./60 + 59./3600) # North: 0, 14, 15, 16, 17, 18
gbt_lon = -1*np.radians(79. + 50./60 + 23./3600)
gbt_D_to_IC = 1.801
parkes_lat = -1*np.radians(33.) # North: 1, 2, 19
parkes_lon = np.radians(148 + 15./60 + 44./3600) # South: ALL (0 - 8)
parkes_D_to_IC = 0.954

icecube = ephem.Observer()
icecube.elevation = 1000
icecube.lon, icecube.lat = 0., np.radians(-90.)

w = True
if w == True: 
    writefile = open('/home/sfahey/public_html/FRB/barycentric_corrections.txt', 'w')
    writefile.write('===================\n|  Northern FRBs  |\n===================\n')

for i in range(29):
    obs = ephem.Observer()
    obs.elevation = 1000
    if i in np.arange(3,14): obs.lon, obs.lat, site, D = arecibo_lon, arecibo_lat, 'Arecibo', arecibo_D_to_IC
    elif i in [0,14,15,16,17,18,19]: obs.lon, obs.lat, site, D = gbt_lon, gbt_lat, 'Green Bank', gbt_D_to_IC
    elif i in [1,2]: obs.lon, obs.lat, site, D = parkes_lon, parkes_lat, 'Parkes', parkes_D_to_IC
    elif i > 19: obs.lon, obs.lat, site, D = parkes_lon, parkes_lat, 'Parkes', parkes_D_to_IC
    obs.date, icecube.date = ephem.Date(t_obs[i]), ephem.Date(t_obs[i])
    
    ice_ra, ice_dec = icecube.radec_of(0., np.pi/2) # RA and Dec of IceCube's zenith at time t
    obs_ra, obs_dec = obs.radec_of(0., np.pi/2) # RA and Dec of observatory's zenith at time t

    ice_dot_FRB = ephem.separation([float(ephem.degrees(ice_ra)), float(ephem.degrees(ice_dec))],[ra[i], dec[i]])
    obs_dot_FRB = ephem.separation([float(ephem.degrees(obs_ra)), float(ephem.degrees(obs_dec))],[ra[i], dec[i]])

    s = math.cos(float(ice_dot_FRB)) - math.cos(float(obs_dot_FRB))
    r_Earth = 6.371e6 # Earth mean radius in meters
    light_time = (s*r_Earth/3.e8)*1.e3 # Difference in ms
    if w == True:
        if i == 20: writefile.write('\n===================\n|  Southern FRBs  |\n===================\n')
        writefile.write("\nFRB_Dec = %f\nSite = %s\nObs. Time = %s\nsep(Obs,FRB) = %s\nsep(Ice,FRB) = %s\nBarycentric Corr. = %f ms\n"%(dec[i]*180./np.pi, site, obs.date, obs_dot_FRB, ice_dot_FRB, -1*light_time))

if w == True:
    writefile.write("\nNOTE: Observation time + Barycentric Correction = Time at IceCube via plane-wave propagation")
    writefile.close()
