#!/bin/bash

clear


MESHPATH="example_data"
MESHNAME="LAbody"
ENDOMESH="LAendo"
LAwall_tag=1


echo "extracting LA wall from mesh..."

cmd="meshtool extract mesh -msh=${MESHPATH}/LAmesh -tags=${LAwall_tag} -submsh=${MESHPATH}/regions_tmp/${MESHNAME} -ifmt=carp_txt -ofmt=carp_txt"

eval $cmd
 

echo "Generating volume element centres..."
cmd="GlElemCenters -m ${MESHPATH}/regions_tmp/${MESHNAME} -o ${MESHPATH}/${MESHNAME}_ECs.pts"
echo $cmd
eval $cmd 

echo "Loop over volume elements and assign best region label based on endo region map"
cmd="python get_regions/project_regions.py ${MESHPATH}/${ENDOMESH}_ECs.pts ${MESHPATH}/${MESHNAME}_ECs.pts ${MESHPATH}/regions_tmp/new_tags.dat ${MESHPATH}/regions_tmp"
echo $cmd
eval $cmd  

echo "converting to vtu..."
cmd="GlVTKConvert -m ${MESHPATH}/regions_tmp/${MESHNAME} -e ${MESHPATH}/regions_tmp/myo_regions.dat -o ${MESHPATH}/regions_tmp/LAbody_regions --trim-names"
eval $cmd

echo "inserting LA body data on full mesh..."
cmd="meshtool insert data -msh=${MESHPATH}/LAmesh -submsh=${MESHPATH}/regions_tmp/${MESHNAME} -submsh_data=${MESHPATH}/regions_tmp/myo_regions.dat -odat=${MESHPATH}/regions_tmp/la_regions.dat -mode=1"
eval $cmd

echo "converting to vtu..."
cmd="GlVTKConvert -m ${MESHPATH}/LAmesh -e ${MESHPATH}/regions_tmp/la_regions.dat -o ${MESHPATH}/regions_tmp/LAmesh_regions --trim-names"
eval $cmd
