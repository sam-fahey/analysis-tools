# analysis-tools

This folder is for software tools that, although written to solve specific problems in my analyses, may be applied to a broader set of analyses.

## Topocentering

![Depiction of time-difference between signal arrival at observatories at different locations on Earth](Topocentric_correction.png)

For a transient correlation analysis at timescales less than 1 second, we need to account for the non-negligible distance difference from the source to Observatory A and to Observatory B. For example, assume a telescope at the North Pole detected an astrophysical event at time t0 and declination +90. In an IceCube follow-up search, if the hypothesis is that the electromagnetic and neutrino emissions were simultaneous, the time of maximum temporal correlation is instead t0 + 42 ms: the neutrinos will take an additional 42 ms to travel through the Earth and trigger the detector.

* topocentering.py calculates the correction value given the event coordinates, time at and coordinates of observatory of initial detection, and coordinates of follow-up observatory.
