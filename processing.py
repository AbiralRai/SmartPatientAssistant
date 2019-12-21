#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 19:30:56 2019

@author: abiralrai
"""
import wfdb
import numpy as np
import glob
from scipy import signal
from wfdb import processing

def get_records(route,format):
    """ Get paths for data in data/mit/ directory """
    
    # There are 3 files for each record
    # *.atr is one of them
    paths = glob.glob(f'{route}/*.{format}')
    print(route)
    print(format)
    # Get rid of the extension
    paths = [path[:-4] for path in paths]
    paths.sort()

    return paths


def getSignal(records):
    """ Returns all records of each subjects"""
    allSignals = []
    allFields = []
    for e in records:
        signals, fields = wfdb.rdsamp(e ,channels = [0], sampto=600000)
        allSignals.append(signals)
        allFields.append(fields)
    return allSignals, allFields

def getAnn(records, ext):
    """Returns all annotation of each subjects """
    allAnns = []
    for ann in records:
        annotation = wfdb.rdann(ann, ext, sampto=600000)
        allAnns.append(annotation)
    return allAnns


def beat_annotations(annotation):
    """ Get rid of non-beat markers """
    """'N' for normal beats. Similarly we can give the input 'L' for left bundle branch block beats. 'R' for right bundle branch block
        beats. 'A' for Atrial premature contraction. 'V' for ventricular premature contraction. '/' for paced beat. 'E' for Ventricular
        escape beat."""
    
    good = ['N']   
    ids = np.in1d(annotation.symbol, good)

    # We want to know only the positions
    annotation.sample =  annotation.sample[ids] #This returns only 'N' samples

    return annotation


def allNewSignal(records, signal, anno):
    """ Process all records to the target frequency containing symbol ['N'] \n
        Records = records of all dataset readings \n
        Signal = records of all signals \n
        Annos = Annotation of all records
    """
    newSignals = []
    newAnnos = []
    for i, e in enumerate(records):
        # Processing each sample frequency
        eachSignals, eachAnnos = processing.resample_singlechan(signal[i][:, 0], anno[i], fs, fs_target)
        newSignals.append(eachSignals)
        eachNAnnos = beat_annotations(eachAnnos)
        newAnnos.append(eachNAnnos)
    return newSignals, newAnnos

#------------------- CHF Unhealthy ECG Below --------------------


# CHF Unhealthy beats
chfRecords = get_records('files', 'ecg')

# Get all signals and fields
signals, fields= getSignal(chfRecords)

# CHF Anno
annos = getAnn(chfRecords, 'ecg')



fs = fields[0]['fs'] # Original frequency
fs_target = 128 # Target frequency


# New Unhealthy signal 128 Frequency!!
newSignals, newAnnos = allNewSignal(chfRecords, signals, annos) 



#------------------- MIT-BIH Healthy ECG Below --------------------

# Healthy ECG
mitRecords = get_records('MIT-BIH-Healthy', 'atr')

# MIT signals and fields
mitSignals, mitFields = getSignal(mitRecords)

# MIT Anno
mitAnnos = getAnn(mitRecords, 'atr')

newMitSignals, newMitAnnos = allNewSignal(mitRecords,mitSignals, mitAnnos)

