#### import the simple module from the paraview
from paraview.simple import *
import sys, getopt, subprocess, vtk

def main(argv):
    inputfile = ''
    closedmesh = ''
    mitralannulus = ''
    verbose = 1
    try:
        opts, args = getopt.getopt(argv,"shi:c:m:",["ifile=","closedmesh=","mitralannulus="])
    except getopt.GetoptError:
        print 'LAstatistics.py -i <inputfile> -c <closedmesh> -m <mitralannulus> -s'
        print '    <inputfile>      path to input file'
        print '    <closedmesh>     path to output file for the closed left atrium'
        print '    <mitralannulus>  path to output file for the mitral annulus'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'LAstatistics.py -i <inputfile> -c <closedmesh> -m <mitralannulus> -s'
            print '    <inputfile>      path to input file'
            print '    <closedmesh>     path to output file for the closed left atrium'
            print '    <mitralannulus>  path to output file for the mitral annulus'
            sys.exit(2)
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-c", "--closedmesh"):
            closedmesh = arg
        elif opt in ("-m", "--mitralannulus"):
            mitralannulus = arg
        elif opt == '-s':
            verbose = 0
    if verbose == 1:
        print '> Input file is                        ', inputfile
        print '> Closed mesh file is                  ', closedmesh
        print '> Mitral annulus file is               ', mitralannulus

    # open the input file
    reader = OpenDataFile(inputfile)
    if verbose == 1:
        print '> OpenDataFile ......................... done'

    # create a new 'Feature Edges'
    featureEdges1 = FeatureEdges(Input=reader)
    if verbose == 1:
        print '> FeatureEdges ......................... done'

    # Properties modified on featureEdges1
    featureEdges1.FeatureEdges = 0
    featureEdges1.NonManifoldEdges = 0
    if verbose == 1:
        print '> Modifying feature edges properties ... done'

    # create a new 'Delaunay 2D'
    delaunay2D1 = Delaunay2D(Input=featureEdges1)
    if verbose == 1:
        print '> Delaunay2D ........................... done'

    # create a new 'Extract Surface'
    extractSurface1 = ExtractSurface(Input=delaunay2D1)
    if verbose == 1:
        print '> ExtractSurface ....................... done'

    # save data
    if mitralannulus:
        SaveData(mitralannulus, proxy=extractSurface1)
        if verbose == 1:
            print '> Save mitral annulus data ............. done'

    # create a new 'Append Geometry'
    appendGeometry1 = AppendGeometry(Input=[reader, extractSurface1])
    if verbose == 1:
        print '> AppendGeometry ....................... done'

    # create a new 'Extract Surface'
    extractSurface2 = ExtractSurface(Input=appendGeometry1)
    if verbose == 1:
        print '> ExtractSurface ....................... done'

    # save data
    if closedmesh:
        SaveData(closedmesh, proxy=extractSurface2)
        if verbose == 1:
            print '> Save closed mesh data ................ done'

    # output the parameters
    print 'LEFT ATRIAL PROPERTIES'
    subprocess.call(["MassProperties", closedmesh])

    print '\nMITRAL VALVE PROPERTIES'
    subprocess.call(["MassProperties", mitralannulus])

if __name__ == "__main__":
    main(sys.argv[1:])
