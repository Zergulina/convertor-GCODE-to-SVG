import os
import zipfile
import svgwrite

from parserGcode import parseGcode

def toSVGConv(pathToGCodeFile, pathToSVG):
    os.mkdir(pathToSVG)

    prevCoord = [0,0,0]
    newCoord = [0,0,0]
    prevCom = ""
    newCom = ""
    isInch = 0

    z = 0

    dwg = svgwrite.Drawing(f'{pathToSVG}/0.svg')

    gcodeList = parseGcode(pathToGCodeFile)

    withCom = False
    for i in gcodeList:
        
        for k in i:
            if 'Z' in k and float(k[1:]) != z:
                z = float(k[1:])
                dwg = svgwrite.Drawing(f'{pathToSVG}/{z}.svg')

        if i[0][0] in "GPMDLIJKL":
            newCom = i[0]
            withCom = True
        else:
            newCom = prevCom[:]
            withCom = False

        if newCom in ["G00","G0"]:
            print(i)
            for k in i:
                if k[0] == 'X':
                    prevCoord[0] = float(k[1:])
                if k[0] == 'Y':
                    prevCoord[1] = float(k[1:])
                if k[0] == 'Z':
                    prevCoord[2] = float(k[1:])
            if withCom == True:
                prevCom = i[0][:]


        if newCom in ["G01", "G1"]:
            changed = False
            for k in i:
                if k[0] == 'X':
                    newCoord[0] = float(k[1:])
                    changed = True
                if k[0] == 'Y':
                    newCoord[1] = float(k[1:])
                    changed = True
                if k[0] == 'Z':
                    newCoord[2] = float(k[1:])
                    changed = True
            
            if changed == True:
                dwg.add(dwg.line((prevCoord[0],prevCoord[1]), (newCoord[0],newCoord[1]), stroke=svgwrite.rgb(10, 10, 16, '%')))
                prevCoord = newCoord[:]
            if withCom == True:
                prevCom = i[0][:]
        dwg.save()
