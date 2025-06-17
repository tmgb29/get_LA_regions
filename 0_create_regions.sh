#!/bin/bash

clear

MESH_PATH="example_data"
UAC_PATH="${MESH_PATH}/UAC"
UAC_MESH="Labelled_Coords_2D_Rescaling_v3_C.elem"
UAC_ENDOMESH="LA_endo"


echo "*****************************"
echo "converting uac mesh to vtk"
echo "*****************************"
cmd="meshtool convert -imsh=${UAC_PATH}/${UAC_MESH} -omsh=${MESH_PATH}/endo_UAC -ifmt=carp_txt -ofmt=vtk"
eval $cmd 


echo "*****************************"
echo "converting uac endo mesh to vtk"
echo "*****************************"
cmd="meshtool convert -imsh=${UAC_PATH}/${UAC_ENDOMESH} -omsh=${MESH_PATH}/LAendo -ofmt=carp_txt -ifmt=vtk"
eval $cmd 

echo "*****************************"
echo "converting uac endo mesh to vtk"
echo "*****************************"
cmd="meshtool convert -imsh=${MESH_PATH}/LAendo -omsh=${MESH_PATH}/LAendo -ifmt=carp_txt -ofmt=vtk"
eval $cmd 

echo "*****************************"
echo "creating initial regions on endo mesh and UACs"
echo "*****************************"
cmd="python get_regions/regions_uac.py --file_path ${MESH_PATH}"
eval $cmd 
