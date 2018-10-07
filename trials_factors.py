#!/usr/bin/env python
import time
import numpy as np
from scipy.stats import poisson

def trigger_threshold(p, l):
  ''' Calculates number of counts necessary to
      exceed p-value significance with average lambda

      Arguments:
  p -- p-value threshold
  l -- average of poisson distribution
  '''
  time_trigger = time.time()
  if p < 0.5:
    k = l - 1
    while poisson.cdf(k, l) < (1.-p): k += 1
    return k+1 
  else:  
    k = 0
    while poisson.cdf(k, l) < (1.-p): k += 1
    return k+1

def ever_exceeds(window_l, window_thresh):
  ''' Simulates an expanding search;
      returns whether any window met pre-trial threshold

      Arguments:
  window_l      -- list of averages in windows
  window_thresh -- list of thresholds to meet p-value
  '''
  assert len(window_l) == len(window_thresh), "Length of lambdas not equal to length of thresholds"
  
  running_total = 0
  for i in range(len(window_l)):
    if i == 0: temp_l = window_l[i]
    else: temp_l = window_l[i] - window_l[i-1]
    running_total += np.random.poisson(temp_l, 1)[0]
    if running_total >= window_thresh[i]: return True  
  return False


def expanding_windows(p, l, factor, n_windows, n_reals, clock=False):
  ''' Returns trials factor correction for
      observation of minimum pre-trial p-value
      in expanding-time-window search

      Arguments:
  p         -- minimum pre-trial p-value observed among time windows
  l         -- average counts in first window 
  factor    -- factor by which subsequent windows expand
  n_windows -- iterations of expansion
  n_reals   -- realizations of unique expansions
  clock     -- output computation time
  '''

  time0 = time.time()

  window_l = [ l * (factor**x) for x in range(n_windows) ]
  window_thresh = [ trigger_threshold(p, x_l) for x_l in window_l ]
  
  total_exceed = 0
  for i in range(n_reals):
    if ever_exceeds(window_l, window_thresh): total_exceed += 1  

  post_p = 1.*total_exceed / n_reals
  if clock: print "Expanding windows: %.3f s"%(time.time()-time0)
 
  return {'post_p':post_p, 'trials_factor':post_p/p, 
          'N_exceed':total_exceed, 'N_total':n_reals}


