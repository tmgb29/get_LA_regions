import numpy as np 
import sys
import scipy.spatial as sp
import copy


endo_ECs=sys.argv[1]
la_ECs=sys.argv[2]
endo_regions_file=sys.argv[3]
outpath = sys.argv[4]

print('Reading endo mesh...')

endo_regions = np.loadtxt(endo_regions_file, dtype=float)
endo_regions = endo_regions.astype(int)

print('Done')

print('Reading endo element centres...')
endo_elemC = np.loadtxt(endo_ECs,dtype=float,skiprows=1)
print('Done')


print('Done')

print('Reading vol element centres...')
la_elemC = np.loadtxt(la_ECs,dtype=float,skiprows=1)
print('Done')


endo_distance_tree = sp.cKDTree(endo_elemC)
new_la_regions = np.zeros(len(la_elemC))

for i in range(la_elemC.shape[0]):
	new_la_regions[i] = endo_regions[endo_distance_tree.query(la_elemC[i])[1]]


np.savetxt(outpath +'/myo_regions.dat',new_la_regions,fmt="%g")
