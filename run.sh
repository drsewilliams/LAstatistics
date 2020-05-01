#!/bin/bash

m="__MV__.vtk"
for inputfile in $1/*.vtk; do

    # set up the inputfile and outfile variables
    ifile=${inputfile%.vtk}
    outfile=$ifile$m

    # run the LAstatistics.py programme
    echo -e "\n"
    echo $inputfile
    echo ===================================
    pvpython LAstatistics.py -s -i $inputfile -m $outfile
done
