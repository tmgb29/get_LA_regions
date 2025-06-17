import pyvista as pv
import vtk
import random
import numpy as np
from vtk.util import numpy_support as VN
import argparse



def main(args):

	print(args.file_path)

	mesh = pv.read(args.file_path + '/endo_UAC.vtk')

	endo_mesh = pv.read(args.file_path + '/LAendo.vtk')

	edges = mesh.extract_feature_edges(boundary_edges=True, feature_edges=False, manifold_edges=False)

	if args.show_mesh == True:

		p = pv.Plotter()
		p.add_mesh(mesh, color=True)
		p.add_mesh(edges, color="red", line_width=5)
		p.show()

	# print(edges)
	# print(edges.extract_cells)

	regions = edges.connectivity()
	centers_x = []
	centers_y = []
	# print(regions)
	# print(len(pv.get_array(regions, name="RegionId")))
	for region_id in range(6):
		PV_region = regions.extract_cells(regions["RegionId"]==region_id)
		centers_x = np.append(centers_x,PV_region.center[0])
		centers_y = np.append(centers_y,PV_region.center[1])

	left_indices = []

	for i, x_coord in enumerate(centers_x):
		if x_coord > 0.6:
			left_indices = np.append(left_indices,i)

	left_indices = left_indices.astype(int)
	left_ycoords = np.take(centers_y,left_indices)
	left_idx = np.where(left_ycoords==np.amin(left_ycoords))[0]
	lipv_idx = left_indices[left_idx]

	right_indices = []

	for i, x_coord in enumerate(centers_x):
		if x_coord < 0.4:
			right_indices = np.append(right_indices,i)

	right_indices = right_indices.astype(int)
	right_ycoords = np.take(centers_y,right_indices)
	right_idx = np.where(right_ycoords==np.amax(right_ycoords))[0]
	rspv_idx = right_indices[right_idx]


	###bounds - lipv
	lower_bound = float(centers_y[lipv_idx]) ## ymin
	left_bound = float(centers_x[lipv_idx])  ## xmax


	# ##bounds - rspv
	upper_bound = float(centers_y[rspv_idx]) # ymax
	right_bound = float(centers_x[rspv_idx])  ## xmin

#	print(upper_bound)
#	print(left_bound)
#	

	## Get region cell IDs
	## find the index of cells in this mesh within bounds [xmin, xmax, ymin, ymax, zmin, zmax]

	roof_inds = mesh.find_cells_within_bounds([right_bound, left_bound, lower_bound, upper_bound, 0.0, 0.0])
	lat_inds = mesh.find_cells_within_bounds([left_bound, 1.0, 0.0, 1.0, 0.0, 0.0])
	sept_inds = mesh.find_cells_within_bounds([0.0, right_bound, 0.0, 1.0, 0.0, 0.0])
	post_inds = mesh.find_cells_within_bounds([right_bound, left_bound, 0.0, lower_bound, 0.0, 0.0])
	ant_inds = mesh.find_cells_within_bounds([right_bound, left_bound, upper_bound, 1.0, 0.0, 0.0])


	# Append cell_data to 2D UAC and LA msh
	local_region_ar = np.zeros((mesh.number_of_cells,))

	local_region_ar[ant_inds] = 1.0
	local_region_ar[post_inds] = 2.0
	local_region_ar[sept_inds] = 3.0
	local_region_ar[lat_inds] = 4.0
	local_region_ar[roof_inds] = 5.0

	mesh.cell_data["region_label"] = local_region_ar
	endo_mesh.cell_data["region_label"] = local_region_ar

	mesh.save(args.file_path + '/endo_UAC.vtk')
	endo_mesh.save(args.file_path + '/LAendo.vtk')

	np.savetxt(args.file_path + '/endo_regions.dat',local_region_ar,fmt='%i')


if __name__ == '__main__':

  parser = argparse.ArgumentParser()
  parser.formatter_class = argparse.ArgumentDefaultsHelpFormatter

  parser.add_argument('--file_path', type=str, default='./',
                      help='path to mesh directory')

  parser.add_argument('--show_mesh', dest='show_mesh', default=False, action='store_true',
                      help='select True to display edges on UAC mesh')


  args = parser.parse_args()

  main(args)

