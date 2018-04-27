#!/bin/env python

############################################
# Script to draw a bar chart with evenly space bars on the x-axis
#  - will also put error bars on the bar chart
#
# The user should input all data and options into the script below and
# just run from the command line: python bar_charts.py
#
# Plot will be displayed to the screen and saved as 900dpi file figure.png
#
# Dependencies
#   Python2.7
#
# Python Packages - minimum versions
#   Matplotlib  v2.0
#   Numpy  v1.12.1
############################################

import matplotlib.pyplot as plt
import numpy as np
from math import *

############################################
# User inputs to the script
#
LOGY = False   # Whether or not the y-axis is log10 scale.  Set to True for log scale
NOY = False    # Whether or not the y-axis is even there.  Set to Tru to remove y-axis

Y_LABEL = 'Modulus'   # Y-axis label
Y_UNITS = 'kPa'       # Units on the y-axis

# Data for bars.
# MEAN is the 'height' of the bar
# STDERROR is the error bars (will display both + and - of the same length = STDERROR)
#     - although this variable is called 'STDERROR' is can be whatever you want, its just the
#       length of the error bars
# X_LABELS are the labels on the x-axis to put under each error bar
# COLORS are the error bar colors

MEAN = [12.83,2.04]
STDERROR = [1.80,0.23]
X_LABELS = ['Circum', 'Radial']
COLORS = ['#DD0000','#0000DD']

# Set the font size - may need to change base on how many bars and length of text
FONT_SIZE=22

#
# End of user inputs
############################################



############################################
# Function to label with non exponential notation on the log scale
#
def log_10_product(x, pos):
    if x >= 0.1: return '%3.1f' % (x)
    if x < 0.01: return '%5.3f' % (x)
    return '%4.2f' % (x)
#
# End of log_10_product funtion
############################################

############################################
# Function to set the scale on the y-axis so there isn't a bunch of zeros
# Based on input data, the scale will either be set to k or M or left alone
#
def scale( data, base_units ):
    ret = {}
    tens = log10( np.max( data ) )
    if tens > 6:
        ret['mult'] = 1000000.0
        ret['units'] = 'M' + base_units
    elif tens > 3:
        ret['mult'] = 1000.0
        ret['units'] = 'k' + base_units
    else:
        ret['mult'] = 1.0
        ret['units'] = base_units
            
    return ret
#
# End of scale funtion
############################################
        


############################################
# Entry point into the program
#
if __name__ == '__main__':

# Put uer inputs into Numpy arrays
    labels = np.array( X_LABELS  )
    values = np.array( MEAN )
    stderr = np.array( STDERROR )

# Set up the font
    font = { 'family' : 'Arial', 'weight' : 'normal','size'   : FONT_SIZE }
    plt.rc( 'font', **font )

# Format the y-axis 
    formatter = plt.FuncFormatter( log_10_product )
    sc = scale( values, Y_UNITS )

# Make figure
    fig = plt.figure(figsize=(10,6))
    ax1 = fig.add_subplot( 111 )
    if not NOY:
        if  Y_UNITS != '':
            ax1.set_ylabel( '%s (%s)' % ( Y_LABEL, sc['units'] ) )
        else:
            ax1.set_ylabel( '%s' % Y_LABEL )

    xlocations = np.arange( len(values) ) + 0.5
    width = 0.5
    ax1.bar(xlocations, values/sc['mult'], yerr=stderr/sc['mult'], width=width, color=COLORS, error_kw=dict(elinewidth=1.5, ecolor='black'), linewidth=0,log=LOGY)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.yaxis.set_ticks_position('left')
    ax1.xaxis.set_ticks_position('bottom')
    plt.xticks(xlocations, labels)
    plt.xlim(0, xlocations[-1]+width*2) 
    if LOGY:
        ax1.yaxis.set_major_formatter( formatter )
    if NOY:
        ax1.yaxis.set_major_formatter(plt.NullFormatter())

    fig.savefig( 'figure.png', dpi=900 )
    plt.show()