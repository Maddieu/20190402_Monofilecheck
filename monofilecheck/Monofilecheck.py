import os
import time
#import pandas as pd
import sys

#os.chdir("D:\\Messdaten\\2016_05 Electrospray FeBpy FeAcac\\2019_04_25_PythonAnalyzerAnalysis_rawdata")

#os.chdir("D:\\Messdaten\\2019_03_ESI_FeBpy\\20190321_MnAcac_Python")

masslist = []
deltamasslist = []
monofilecontent = []
filenameslist = []

fileindex = 0
firstmonoline = 0

###################################################
###################################################
###################################################
#
#
#
#
# Durchlaufe alle (Unter)Ordner des derzeitigen Verzeichnisses
# suche dort nach _Mono.txt Dateien
# Suche in diesen Dateien die Zeile # LEGEND und die Zeile (mind. 2 Zeilen weiter) welche mit # ---- startet
#       um das Ende der Legende festzustellen. Die Zeile danach ist die erste "firstmonoline" Zeile mit Daten.
# Lese dann alle Zeilen und (Elemente in den Zeilen) ein.
#
#   Struktur des Monofilecontents am Ende:
#       Erste Listenebene:      [Monofile1, Monofile2, Monofile3, ...]
#       Zweite Listenebene:     in Monofile1:   [Line1, Line2, Line3, ...]
#       Dritte Listenebene:     in Line1:       [Element1, Element2, Element3, ...]
#
#   File1
#       Line1
#           Element1
#           Element2
#           Element3
#       Line2
#           Element1
#           Element2
#           Element3
#       Line3
#           Element1
#           Element2
#           Element3
#   File2
#       ...
#
#
#   monofilecontent[file][line][element]
#
#
#
#   The name of the files (File1, File2, ...) will be listed in the list: "filenameslist"
#
#
#
####################################################################################################
#
#   20190524
#
#   output file is now written with so called: f strings:
#       file.write(f'{"FirstEnergy[eV]": <17}')
#                  the f' ... '  is the synthax for an fstring
#
#                       strings inside the ' ' have to be denoted with " "
#
#                                       the : is a more precise definition for the argument given before
#                                           < means that the text orientation will start on the left side ( right: > )
#                                           <17 means that the column will be 17 characters broad and
#                                                           the filling will start from the left side
#
#
#
###################################################
###################################################
###################################################


for currentdir, dirlist, filelist in os.walk(os.curdir):
    for filename in filelist:
        if filename.endswith('_Mono.txt') is True:
            print('found file', fileindex, filename)
            monofilecontent.append([])                      # gib dem Monofilecontent einen weiteren Eintrag => Eine Datei mehr

            with open(currentdir +'\\' + filename, 'r') as currentmonofile:
                monofiletemp = currentmonofile.readlines()  # gesamten inhalt der geöffneten Datei einlesen
                filenameslist.append(filename)

            afterlegendstart = False
            afterlegendend = False                          # Hier befinden wir uns noch in dem Header / vor der Legende

            for linenumber in range(monofiletemp.__len__()):    #durchlaufe alle Lines

                if monofiletemp[linenumber].startswith("# massfilter mass"):
                    masslist.append(float(monofiletemp[linenumber].split()[-1]))
                if monofiletemp[linenumber].startswith("# massfilter dM"):
                    deltamasslist.append(float(monofiletemp[linenumber].split()[-1]))
                if monofiletemp[linenumber-3].startswith('# LEGEND'):       #Anfang der Legende vor 3 Zeilen gefunden
                    afterlegendstart = True
                if (afterlegendstart == True) and monofiletemp[linenumber - 1].startswith('# -----'):   # Ende der Legende
                    afterlegendend = True
                    firstmonoline = linenumber      #erste Zeile der eigentlichen Mono-File-Daten

                # Die Konstrukte hier mit -1 und -3 dienen dazu, sich nicht von der "# ----" Zeile direkt hinter
                # "# LEGEND" ins Boxhorn jagen zu lassen
                # das -1 dient im besonderen dazu, dass die 'Line Nr. 0' nicht "# ----" ist, sondern die erste Daten Line
                # folgend wird nun sicher gestellt, dass wir hinter der #LEGEND und hinter der #---- sind und somit den Header verlassen haben



                if (afterlegendstart == True) and (afterlegendend == True):
                    monofilecontent[fileindex].append([])                       #für jede neue Zeile wird ein neuer Eintrag(Zeile) angelegt
                    for element in monofiletemp[linenumber].split('\t'):        # die eingelesene monofiletemp-Zeile wird in die Elemente gesplittet
                        monofilecontent[fileindex][linenumber - firstmonoline].append(element)  # und das entsprechende Element ins des Fileindexes und der Linenr. geschrieben

            fileindex = fileindex + 1

print(monofilecontent)

print(filenameslist)
"""
for filenumber in range(monofilecontent.__len__()):
    #print(monofilecontent[filenumber])
    for line in range(monofilecontent[filenumber].__len__()):
        #print(monofilecontent[filenumber][line])
        for element in range(monofilecontent[filenumber][line].__len__()-1):
            print(monofilecontent[filenumber][line][element], end = "\t")

        print()
    print('\n')
"""









def decideedge(firstenergy):

#   Have a tolerance around this first point of 40 eV
#       Check if the difference between firstPointEnergyOfTheScan/Monofile and the UsualEnergyForAnEdge is smaller than 40 eV
#       then the scan is accounted to this edge

    def inrange(energy, element):
        if abs(float(energy) - element) < 40:
            return True
        else:
            return False

    #print('#### testing for elements')
    if inrange(firstenergy, 280) is True:
        return str('Carbon Edge')
    elif inrange(firstenergy, 700) is True:
        return str('Iron Edge')
    elif inrange(firstenergy, 770) is True:
        return str('Cobalt Edge')
    elif inrange(firstenergy, 530) is True:
        return str('Oxygen Edge')
    elif inrange(firstenergy, 630) is True:
        return str('Manganese Edge')
    elif inrange(firstenergy, 400) is True:
        return str('Nitrogen Edge')
    elif inrange(firstenergy, 200) is True:
        return str('Chlorine Edge')
    elif inrange(firstenergy, 1230) is True:
        return str('Terbium Edge')
    elif inrange(firstenergy, 1285) is True:
        return str('Dysprosium Edge')
    else:
        return str('Edge unknown')





with open('_OverviewMonoFiles.txt', 'w') as file:

#
#
#       writing the header
#
#


    columnstring = 'Filename'
    columnwidth = columnstring.__len__()
    file.write(f'{"Filename": <30}')
    file.write(f'{"FirstEnergy[eV]": <17}')
    file.write(f'{"LastEnergy[eV]": <16}')
    file.write(f'{"Steps[eV]": <11}')
    file.write(f'{"EnergySlit[eV]": <16}')
    file.write(f'{"Bandwidth[eV]": <15}')
    file.write(f'{"Photocurrent[eV]": <18}')
    file.write(f'{"QMS Mass[amu/z]": <17}')
    file.write(f'{"QMS_dM": <9}')
    file.write(f'{"UnduShift[mm]": <15}')
    file.write(f'{"PhotonFlux[ph/s]": <21}')
    file.write(f'{"TempSE[eV]": <12}')
    file.write(f'{"pDEFL[mbar]": <13}')
    file.write(f'{"Edge"}')


    file.write('\n')
    #file.write('Filename\tFirstEnergy[eV]\tLastEnergy[eV]\tSteps[eV]\tEnergySlit[um]\tBandwidth[meV]\tPhotocurrent[A]\tQMS Mass[amu/z]\tPhotonFlux[ph/s]\ttempSE[K]\tpDEFL[mbar]\tEdge')

    file.write('\n')

    for fileindex in range(monofilecontent.__len__()):
        try:

            #
            # definition area
            #

            firstenergy = monofilecontent[fileindex][0][3]
            lastenergy = monofilecontent[fileindex][-1][3]
            stepwidth = round(float(monofilecontent[fileindex][1][3]) - float(monofilecontent[fileindex][0][3]), 3)
            energyslit = monofilecontent[fileindex][0][6]
            bandwidth = monofilecontent[fileindex][0][7]
            photocurrent = monofilecontent[fileindex][0][5]
            mass = str(masslist[fileindex])
            deltamass = str(deltamasslist[fileindex])
            photonflux = str(float(monofilecontent[fileindex][0][21]))
            tempSE = str(float(monofilecontent[fileindex][0][11]))
            pdefl = monofilecontent[fileindex][0][16]
            undushift = str(round(float(monofilecontent[fileindex][0][9])))

            #
            #       note here, that the undulator shift is rounded!!
            #       it shall only indicate if the scan was hor or neg/pos polarization
            #

            edge = decideedge(firstenergy)


            file.write(f'{filenameslist[fileindex]: <30}')
            #                  1234567890123456789
            file.write(f'{firstenergy: <17}')
            file.write(f'{lastenergy: <16}')
            file.write(f'{stepwidth: <11}')
            file.write(f'{energyslit: <16}')
            file.write(f'{bandwidth: <15}')
            file.write(f'{photocurrent: <18}')
            file.write(f'{mass: <17}')
            file.write(f'{deltamass: <9}')
            file.write(f'{undushift: <15}')
            file.write(f'{photonflux: <21}')
            file.write(f'{tempSE: <12}')
            file.write(f'{pdefl: <13}')

            file.write(f'{edge}')

            file.write('\n')




            pass
        except Exception as errorcode:
            #errorcode2 = sys.exc_info()
            print('error:', errorcode)
            with open('_Errorlog.txt', 'w') as errorfile:
                errorfile.write('in File:\t' +  filenameslist[fileindex] + '\t\t Error:\t' + str(errorcode))
            file.write('\n')


    dothis = False


    if dothis == True:
        for fileindex in range(monofilecontent.__len__()):
            try:
                #Write File Name
                file.write(filenameslist[fileindex] + "\t")

                firstenergy = monofilecontent[fileindex][0][3]
                file.write(firstenergy + "\t")

                lastenergy = monofilecontent[fileindex][-1][3]
                file.write(lastenergy + "\t")

                stepwidth = round(float(monofilecontent[fileindex][1][3])-float(monofilecontent[fileindex][0][3]), 3)
                #stepwidth = float(monofilecontent[fileindex][1][3])-float(monofilecontent[fileindex][0][3])
                file.write(str(stepwidth) + "\t")

                energyslit = monofilecontent[fileindex][0][6]
                file.write(energyslit + "\t")

                bandwidth = monofilecontent[fileindex][0][7]
                file.write(bandwidth + "\t")

                photocurrent = monofilecontent[fileindex][0][5]
                file.write(photocurrent + "\t")

                mass = str(masslist[fileindex])
                file.write(mass + "\t")

                deltamass = str(deltamasslist[fileindex])
                file.write(deltamass + "\t")

                photonflux = monofilecontent[fileindex][0][21]
                file.write(photonflux + "\t")

                tempSE = monofilecontent[fileindex][0][11]
                file.write(tempSE + "\t")

                pdefl = monofilecontent[fileindex][0][16]
                file.write(pdefl + "\t")

                undushift = monofilecontent[fileindex][0][9]
                file.write(undushift + "\t")

                edge = decideedge(firstenergy)
                file.write(edge + "\t")


                file.write('\n')
            except:
                errorcode = sys.exc_info()
                print('error:', errorcode)
                with open('_Errorlog.txt', 'w') as errorfile:
                    errorfile.write('error:\t' + str(errorcode))
                file.write('\n')


    #print('currentdir:', currentdir)
    #print('dirlist:', dirlist)
    #print('filelist:', filelist)
    #print()


