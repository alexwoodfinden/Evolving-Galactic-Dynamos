The following is a python program written to convert output  from a MAPLE script that produces model rotation measure maps for dynamo solutions, outputted as a .csv file, to a fits image (see Sect. \ref{sect:imp}).  The program uses a template fits image to match the image to the same region of the sky and uses the same header as the template file.  This script needs to be ran from within the Casa shell.  This script has been tested using Casa version 4.7 and Python 2.7.  Parameters to change are located at the top of the file.

Inputs needed: model rotation measure maps output as .csv files, template image that will be used as the observational comparison, galaxy diameter (used to scale model image to the correct size).

Output: model rotation measure map that has been regridded to make the observational template image in .fits format.
