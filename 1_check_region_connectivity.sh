#!/bin/bash

clear


OUTPATH="example_data"
INNAME="LAendo"
MESHNAME="LAendo_regions"
MESHTAGS='parfiles/LAmesh_w_regions_input_tags.json'


echo "*****************************"
echo "calculating endo element centers"
echo "*****************************"
cmd="GlElemCenters -m ${OUTPATH}/${INNAME} -o ${OUTPATH}/${INNAME}_ECs.pts"
echo $cmd
eval $cmd 


echo "*****************************"
echo "creating temp region directory"
echo "*****************************"
cmd="mkdir -p ${OUTPATH}/regions_tmp"
eval $cmd


echo "*****************************"
echo "creating region tagged endo mesh"
echo "*****************************"
cmd="python get_regions/replace_tags.py --mesh_path ${OUTPATH} --mesh_name ${INNAME} --out_path ${OUTPATH}/regions_tmp --out_name ${MESHNAME} --tag_file ${OUTPATH}/endo_regions.dat"
eval $cmd


echo "*****************************"
echo "extracting regions on endo"
echo "*****************************"

cmd="python get_regions/correct_regions_endo.py --mesh_settings ${MESHTAGS} --meshname ${OUTPATH}/regions_tmp/${MESHNAME} --output_folder ${OUTPATH}"
eval $cmd


echo "*****************************"
echo "correcting any floating regions on endo"
echo "*****************************"

cmd="python get_regions/determine_floating.py --endo_mesh ${MESHNAME} --tag_file ${OUTPATH}/endo_regions.dat --endo_ECs ${OUTPATH}/${INNAME}_ECs.pts --output_folder ${OUTPATH}/regions_tmp"
eval $cmd
