# This program was created for Pro-Mold-EPS in Poznań
# by Anton Altynbaev (altynbajew@gmail.com) from OMNIMECH SP. Z O.O.
# in 2020
# v 1.0

import os, sys

def CreateReport(LN,LD,TLN,TLD,qcnc,uwagi):
    beginning = '''
        <table style="width: 100%;" border="1">
        <tbody>
        '''
    quantity_text = '''Ilosc sprawdzonych plikow: '''
    quantity=str(qcnc)
    uwagi_list=[str(s)for s in uwagi]
    uwagi_print=''''''.join(uwagi_list)
    table_header='''
        <tr>
        <td>Narzedzie</td>
        <td>Dlugosc, mm</td>
        </tr>'''
    print_instruments=str()
    ind=0
    for nar in TLN:
        print_instruments=print_instruments + '''<tr> <td>''' + nar + '</td> <td>' + str(TLD[ind]) + '</td> </tr>'
        ind+=1
    next_line='''<br>'''
    ending = '''
        </tbody>
        </table>
        '''

    
    file = open("Report.html","w")
    file.write(beginning)
    file.write(quantity_text)
    file.write(quantity)
    file.write(next_line)
    file.write(uwagi_print)
    file.write(next_line)
    file.write(table_header)
    file.write(print_instruments)
    file.write(ending)
    file.close()
    return



all_files = os.listdir()                    #LIST of all files in the dir   
qcnc = 0                                        #initial state for quantity of 'nc' files in the dir
LN = list()                                         #declare of empty Lista Narzędzi
LD = list()                                       #declare of empty Lista Dlugosci
for obj in all_files:                           #pick one-by-one NAMES of files in the dir
    ext = os.path.splitext(obj)[-1].lower()     #take file extension and lowercase it
    if ext == ".nc":                                #check if extension is 'nc'
        qcnc += 1                                     #increment the counter of 'nc' files
        with open(obj) as fp:                              #open each nc-file
           Zmax = 0                                        #reset max Z coordinate
           for cnt, line in enumerate(fp):                           #read file line-by-line
               line = line.translate({ord(i): None for i in '()\n'})      #delete brackets and 'end of the line' from line
               lowerline = line.lower()                                  #lowercase the line
               if (lowerline.find('frez') != -1):                       #checking used instrument
                   LN.append(line)                                      #add the instrument to Lista Narzędzi
               if (lowerline.find('wiertlo') != -1):
                   LN.append(line)
               if (lowerline.find('glowica') != -1):
                   LN.append(line)
               if (lowerline.find('rozwiertak') != -1):
                   LN.append(line)
               if (lowerline.find('z-') != -1):
                   i = lowerline.find('z-')+2             #find start position of Z coordinate in the line
                   zstr=lowerline[i:]                   #cut everything before Z coordinates
                   j = zstr.find('.')               #find end of integer part of Z coordinates in the line
                   zstr=zstr[:j]                        #cut everything after Z coordinate
                   Z = int(zstr)                      #turn Z into int
                   if Z >= Zmax:                    #that would be the max length of the instrument
                        Zmax=Z             
           LD.append(Zmax)
           if len(LD) != len (LN):                #check if a file contain instrument description
               LN.append('brak')                #if aforenamed "not" then add "empty"

TLN = list()          #List for declared Instruments w/o duplicates
TLD = list()            #List for lengths of Instruments w/o duplicates
i=0                  
for nar in LN:       #Sorting Lista Narzedzi and deleting duplicates
    if nar in TLN:
        j=TLN.index(nar)
        if LD[i] >= TLD[j]:  #Writing the longest instrument
            TLD[j]=LD[i]         
    else:
        TLN.append(nar)
        TLD.append(LD[i])
    i += 1
    
index=TLN.index('brak')  #Find index of empty instrument
TLN.remove('brak')       #Remove not indicated instrument from Report because it could baffle a worker
del TLD[index]           #Remove length of not indicated instrument
    
uwagi=set()
if 'brak' in LN:
    uwagi.add('''Sa programy bez wskazanego narzedzia<br>''')
for i in LD:
    if i > 70:
        uwagi.add ('''Sa programy glebokogo wiercenia<br>''')

CreateReport(LN,LD,TLN,TLD,qcnc,uwagi)





