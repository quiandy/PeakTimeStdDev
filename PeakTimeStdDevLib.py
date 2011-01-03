from math import pow, sqrt, exp
from copy import copy
from numpy.fft import fft
from numpy import array

# Extracts data from text file and puts it in data structure
def extractRawDataFromFile( inputFile ):
    # Data structure holding raw data extraced from file
    rawCurves = {}
    rawCurves['Time'] = []
    rawCurves['Curves'] = {}
    rawCurves['GlobalCurve'] = []
    
    isRadialFile = False
    
    # Variable holding read lines
    line = ""

    # Searching for line holding columns headers
    while "Time (s)" not in line:
        line = inputFile.readline()
        if line == '':
            return None
    
    # Una volta trovata, salvo in una lista tutti
    # i campi separati da tablature (\t), e li
    # salvo in un array, che conterra' quindi
    # tutti i nomi delle colonne
    line = line.replace('\t\t','\t')
    columnNames = map( stripSpaces, line.split('\t'))

    # Saving column name in data structure
    for columnName in columnNames:
        if columnName != 'Time (s)' and columnName != 'GLOBAL' and columnName != 'ECG : ':
            rawCurves['Curves'][columnName] = []
    
    # Checking if GLOBAL column is present
    if columnNames[7] == 'GLOBAL':
        isRadialFile = False
    else:
        # Radial file, will have to calculate GLOBAL Curve
        isRadialFile = True

    # Reading lines from file one at a time
    line = inputFile.readline()

    while line != "":
        valueMatrixLine = []
        line = line.replace('\t\t','\t')
        # Saving each tab separated value as float in a separate list
        for value in line.split('\t'):
            valueMatrixLine.append( float( value ) )

        # Filling time sample column
        rawCurves['Time'].append( valueMatrixLine[0] )
        
        # Filling curve samples
        for col in range (1,len(rawCurves['Curves'])+1):
            rawCurves['Curves'][rawCurves['Curves'].keys()[col -1]].append( valueMatrixLine[col] )
        
        # Filling GLOBAL curve
        if isRadialFile:
            # If radial file no Global curve given, leaving list empty (will be calculated later)
            rawCurves['GlobalCurve'] = []
        else:
            # Using GLOBAL curve taken from file
            rawCurves['GlobalCurve'].append(valueMatrixLine[7])
            
        # Reading next line
        line = inputFile.readline()
    
    return rawCurves, isRadialFile
    
# Copies curve data in new structure eliminating border noise
def stripNoiseFromRawData( rawCurves, startLine, endLine, curvesToLoad ):
    # Data structure holding data betweend zero point passes worth for evaluation
    strippedCurves = {}
    strippedCurves['Curves'] = {}
    
    # Filling strippedCurves data structure only with interesting data
    strippedCurves['Time'] = rawCurves['Time'][startLine:endLine+1]

    # Only loading chosen curves
    for curveName in curvesToLoad:
        strippedCurves['Curves'][curveName] = rawCurves['Curves'][curveName][startLine:endLine+1]
        
    # Calculating global curve
    strippedCurves['GlobalCurve'] = []
        
    for line in range(0, len (strippedCurves['Time'])):
        curveSamples = [ curve[line] for curve in strippedCurves['Curves'].values() ]
        strippedCurves['GlobalCurve'].append( average(curveSamples) )
        
    return strippedCurves

def findCommonZeroPasses( curves ):
    # First pass, search zero pass for each curve
    zeroLinePassMatrix = []

    # Searching columns between the second (the first columns are
    # evaluation times) and the matrixEnd (first or second to last, depending
    # on file type)
    for curve in curves:
        zeroLinePasses = []
        for currentSample in range( 0, len(curve) - 1):
            # Cerco passaggi dallo zero
            if  ( curve[currentSample] == 0.0):
                # If exact zero pass, appending only current line
                zeroLinePasses.append( (currentSample, currentSample) )
            else:
                # If product <0 means one is positive and other is negative
                if curve[currentSample] * curve[currentSample + 1] < 0:
                    # Marking both lines
                    zeroLinePasses.append( ( currentSample, currentSample + 1 ) )

        # Aggiungo alla matrice tutti i passaggi dallo zero rilevati per la singola colonna
        zeroLinePassMatrix.append(zeroLinePasses)

    # Matrix holding all possible tuples for each possible permutation on the zeroLinePassMatrix
    tupleMatrix = [ ]

    # Analyzing all tuples
    for line in zeroLinePassMatrix[0]:
        tupleMatrix.append( [ line ] )

    for col in range(1, len(zeroLinePassMatrix) ):
        l = len(tupleMatrix)

        for h in range(0, len(zeroLinePassMatrix[col]) - 1 ):
            for i in range(0, l):
                tupleMatrix.append( copy(tupleMatrix[i]) )

        for h in range(0, len(zeroLinePassMatrix[col]) ):
            for i in range(0,l):
                tupleMatrix[i + (l*h)].append( zeroLinePassMatrix[col][h] )

    commonZeroPasses = []
    for line in tupleMatrix:
        tempLeft = []
        tempRight = []
        for el in line:
            tempLeft.append(el[0])
            tempRight.append(el[1])

        foundMin = min(tempLeft)
        foundMax = max(tempRight)

        if (foundMin >= foundMax - 2) and (foundMin <= foundMax):
            commonZeroPasses.append( (foundMin,foundMax) )

    zeroLines = []
    # Choosing startLine and endLine from zero pass matrix
    for tuple in commonZeroPasses:
        if tuple[0] == tuple[1]:
            zeroLines.append(tuple[0])

        else:
            if tuple[0] == tuple[1] - 1:
                zeroLines.append(tuple[0])
            else:
                if tuple[0] == tuple[1] - 2:
                    zeroLines.append(tuple[0] + 1)

    # Considerero' solo le righe posteriori al primo passaggio dallo zero di tutte
    # le curve e antecedenti all'ultimo.
    startLine = 0
    endLine = len(curves[0]) - 1
    
    if len(zeroLines) > 0:
        # Checking first zero pass line occurs in first half of valueMatrix
        if zeroLines[0] < len(curves[0]) / 2:
            startLine = zeroLines[0]
            
        if len(zeroLines) > 1:
            # Checking last zero pass line occurs in second half of valueMatrix
            if zeroLines[-1] > len(curves[0]) / 2:
                endLine = zeroLines[-1]
                
    return startLine, endLine


def normalizeTime( times, peakTime ):
    startTime = times[0]
    endTime = times[-1]
    totalTime = endTime - startTime
    
    if ( peakTime == startTime):
        return 100
    else:
        return round ( (((peakTime - startTime) * 100 ) / totalTime) , 2 )

def findPeaks(curves, searchingForMaximums):

    peaks = {}
    globalPeak = {}
        
    # Finding peak values and corresponding times for standard curves
    for curveName in curves['Curves']:

        peaks[curveName] = {}
        pv, pt = getPeak(curves['Curves'][curveName], curves['Time'], searchingForMaximums)
        
        peaks[curveName]['PeakValue'] = pv
        peaks[curveName]['PeakTime'] = pt 

    # Finding peak value and corresponding time for global curve
    pv, pt = getPeak(curves['GlobalCurve'], curves['Time'], searchingForMaximums)
    
    globalPeak['PeakValue'] = pv
    globalPeak['PeakTime'] = pt 
        
    return peaks, globalPeak

def getPeak( curve, times, searchingForMaximums ):
    peakValue = 0
    peakTime = 0
    
    # Mi segno il tempo (prima colonna) delle righe
    # che risultano le minime (o le massime) per una
    # data colonna.
    if searchingForMaximums:
        peakValue = max(curve)
    else:
        peakValue = min(curve)
    
    # Finding time value corresponding to found peak
    peakTime = times[ curve.index( peakValue ) ]    
    
    return peakValue, peakTime
    
def stripSpaces(arg):
    return arg.strip(' ').strip('\n')
    
def average(list):
    if len(list) < 1: return 0
    return sum(list) / len(list)

def standardDeviation(list):
    if len(list) <= 1: return 0
    
    av = average(list)
    
    devSquare = 0
    for val in list:
        devSquare += pow(val - av, 2)

    return sqrt( devSquare / ( len(list) - 1 ) )   

def calculateTUS(strippedCurves):
    f = open('TUS_Debug.log', 'w')
    continuous_component = 0
    first_harmonic = 0

    for currentLine in range(0, len(strippedCurves['Time'])):
        temp = [ curve[ currentLine ] for curve in strippedCurves['Curves'].values() ]
        
        f.write('Line ' + str( currentLine ) + '(counting from cutoff border):\n')
        f.write(str(temp) + '\n')
        
        cont = abs(fft(temp,2).real[0])
        fh = abs(fft(temp,2).real[1])
        
        f.write('FFT Continuous component: ' + str(cont) + '\n')
        f.write('FFT first harmonic: ' + str(fh) + '\n\n')
        
        continuous_component += cont
        first_harmonic += fh
    
    f.close()
    return round( (sqrt(float(continuous_component) / float(continuous_component + first_harmonic)))**3, 6)

def findCrossCorrelationAverage(strippedCurves):
    crossCorrValue = 0
    crossCorrCounter = 0
    
    # Calculating average of every curve
    curveAverages = {}
    curveSqrDen = {}
    
    # Calculating averages and stddev
    for curveName in strippedCurves['Curves'].keys():
        curveAverages[curveName] = average(strippedCurves['Curves'][curveName])
    
        curveSqrDen[curveName] = 0
        for curveValue in strippedCurves['Curves'][curveName]:
            curveSqrDen[curveName] += pow(curveValue - curveAverages[curveName], 2)
    
    crossCorrelationPeaks = []
    crossCorrDebugList = []    

    for colStart in range(0, len(strippedCurves['Curves']) ):
        
        for colEnd in range (colStart + 1, len(strippedCurves['Curves'])):
            
            # Denominator
            curveName1 = strippedCurves['Curves'].keys()[colStart]
            curveName2 = strippedCurves['Curves'].keys()[colEnd]
            
            den = sqrt( curveSqrDen[ curveName1 ] * curveSqrDen[ curveName2 ] )
            
            crossCorrSeries = []    
            # Data structure holding debug information
            crossCorrDebug = {}

            
            for phase in range(0, len(strippedCurves['Time'])):
                num = 0

                for line in range( 0, len(strippedCurves['Time'])):
                    factor1 = strippedCurves['Curves'][curveName1][line] - curveAverages[curveName1]
                    factor2 = strippedCurves['Curves'][curveName2][line - phase] - curveAverages[curveName2]

                    num += factor1 * factor2 
                    
                crossCorrSeries.append( num / den )
            
            crossCorrDebug['Curves'] = (curveName1, curveName2)
            crossCorrDebug['PeakValue'] = round(max(crossCorrSeries),2)
            crossCorrDebugList.append(crossCorrDebug)
            
            crossCorrelationPeaks.append( max(crossCorrSeries) )

    return round( average(crossCorrelationPeaks), 6 ), crossCorrDebugList