#!/usr/bin/python
#
# This is for testing whether there are systematic errors in
# emitter position in the movies generated by simulate.py.
#
# Hazen 12/16
#

import matplotlib
import matplotlib.pyplot as pyplot
import numpy
import sys

import storm_analysis.sa_library.readinsight3 as readinsight3
import storm_analysis.sa_library.ia_utilities_c as utilC

if (len(sys.argv) != 3):
    print("usage: <true locations> <measured locations>")
    exit()

# For converting XY units to nanometers.
pixel_size = 160.0

truth_i3 = readinsight3.I3Reader(sys.argv[1])
measured_i3 = readinsight3.I3Reader(sys.argv[2])

all_dx = None
all_dy = None
all_dz = None
all_x_offset = None
all_y_offset = None
for i in range(truth_i3.getNumberFrames()):
    t_locs = truth_i3.getMoleculesInFrame(i+1)
    m_locs = measured_i3.getMoleculesInFrame(i+1, good_only = False)

    p_index = utilC.peakToPeakIndex(m_locs['xc'], m_locs['yc'], t_locs['xc'], t_locs['yc'])
    dx = numpy.zeros(m_locs.size)
    dy = numpy.zeros(m_locs.size)
    dz = numpy.zeros(m_locs.size)
    x_offset = numpy.zeros(m_locs.size)
    y_offset = numpy.zeros(m_locs.size)
    for i in range(m_locs.size):
        dx[i] = pixel_size * (m_locs['xc'][i] - t_locs['xc'][p_index[i]])
        dy[i] = pixel_size * (m_locs['yc'][i] - t_locs['yc'][p_index[i]])
        dz[i] = m_locs['zc'][i] - t_locs['zc'][p_index[i]]
        x_offset[i] = t_locs['xc'][p_index[i]] - round(t_locs['xc'][p_index[i]])
        y_offset[i] = t_locs['yc'][p_index[i]] - round(t_locs['yc'][p_index[i]])
#        if (i == 0):
#            print(dx[i], dy[i], dz[i], m_locs['xc'][i], t_locs['xc'][p_index[i]])

    if all_dx is None:
        all_dx = dx
        all_dy = dy
        all_dz = dz
        all_x_offset = x_offset
        all_y_offset = y_offset

    else:
        all_dx = numpy.concatenate((all_dx, dx))
        all_dy = numpy.concatenate((all_dy, dy))
        all_dz = numpy.concatenate((all_dz, dz))
        all_x_offset = numpy.concatenate((all_x_offset, x_offset))
        all_y_offset = numpy.concatenate((all_y_offset, y_offset))

print("means and standard deviations (in nm):")
print("mean, std (dx)", numpy.mean(all_dx), numpy.std(all_dx))
print("mean, std (dy)", numpy.mean(all_dy), numpy.std(all_dy))
print("mean, std (dz)", numpy.mean(all_dz), numpy.std(all_dz))
print("")

fig = pyplot.figure()
pyplot.scatter(all_x_offset, all_dx/pixel_size, color = "red")
pyplot.scatter(all_y_offset, all_dy/pixel_size, color = "blue")
pyplot.xlabel("Offset (pixels)")
pyplot.ylabel("Error (pixels)")
pyplot.show()

#
# The MIT License
#
# Copyright (c) 2016 Zhuang Lab, Harvard University
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
