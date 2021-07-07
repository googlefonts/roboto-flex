
font = CurrentFont()

UCaccents = ['Agrave', 'Aacute', 'Acircumflex', 'Atilde', 'Adieresis', 'Aring', 'AE', 'Ccedilla', 'Egrave', 'Eacute', 'Ecircumflex', 'Edieresis', 'Igrave', 'Iacute', 'Icircumflex', 'Idieresis', 'Ntilde', 'Ograve', 'Oacute', 'Ocircumflex', 'Otilde', 'Odieresis', 'Oslash', 'OE', 'Ugrave', 'Uacute', 'Ucircumflex', 'Udieresis', 'Yacute', 'Ydieresis', 'Amacron', 'Abreve', 'Aogonek', 'Aringacute', 'Adblgrave', 'Ainvertedbreve', 'Adotbelow', 'Ahookabove', 'Acircumflexacute', 'Acircumflexgrave', 'Acircumflexhookabove', 'Acircumflextilde', 'Acircumflexdotbelow', 'Abreveacute', 'Abrevegrave', 'Abrevehookabove', 'Abrevetilde', 'Abrevedotbelow', 'Cacute', 'Ccircumflex', 'Cdotaccent', 'Ccaron', 'Dcaron', 'Emacron', 'Ebreve', 'Edotaccent', 'Eogonek', 'Ecaron', 'Edblgrave', 'Einvertedbreve', 'Edotbelow', 'Ehookabove', 'Etilde', 'Ecircumflexacute', 'Ecircumflexgrave', 'Ecircumflexhookabove', 'Ecircumflextilde', 'Ecircumflexdotbelow', 'Gcircumflex', 'Gbreve', 'Gdotaccent', 'Gcommaaccent', 'Gcaron', 'Hcircumflex', 'Itilde', 'Imacron', 'Ibreve', 'Iogonek', 'Idotaccent', 'Idblgrave', 'Iinvertedbreve', 'Ihookabove', 'Idotbelow', 'Jcircumflex', 'Kcommaaccent', 'Lacute', 'Lcommaaccent', 'Lcaron', 'Nacute', 'Ncommaaccent', 'Ncaron', 'Omacron', 'Obreve', 'Ohungarumlaut', 'Ohorn', 'Oogonek', 'Odblgrave', 'Oinvertedbreve', 'Odieresismacron', 'Otildemacron', 'Odotaccentmacron', 'Odotbelow', 'Ohookabove', 'Ocircumflexacute', 'Ocircumflexgrave', 'Ocircumflexhookabove', 'Ocircumflextilde', 'Ocircumflexdotbelow', 'Ohornacute', 'Ohorngrave', 'Ohornhookabove', 'Ohorntilde', 'Ohorndotbelow', 'Racute', 'Rcommaaccent', 'Rcaron', 'Rdblgrave', 'Rinvertedbreve', 'Sacute', 'Scircumflex', 'Scedilla', 'Scaron', 'Scommaaccent', 'Tcedilla', 'Tcaron', 'Tcommaaccent', 'Utilde', 'Umacron', 'Ubreve', 'Uring', 'Uhungarumlaut', 'Uogonek', 'Uhorn', 'Udblgrave', 'Uinvertedbreve', 'Udotbelow', 'Uhookabove', 'Uhornacute', 'Uhorngrave', 'Uhornhookabove', 'Uhorntilde', 'Uhorndotbelow', 'Wcircumflex', 'Wgrave', 'Wacute', 'Wdieresis', 'Ycircumflex', 'Ymacron', 'Ygrave', 'Ydotbelow', 'Yhookabove', 'Ytilde', 'Zacute', 'Zdotaccent', 'Zcaron', 'AEacute', 'Oslashacute', 'Tbar' ]

lcaccents = ['agrave', 'aacute', 'acircumflex', 'atilde', 'adieresis', 'aring', 'ae', 'ccedilla', 'egrave', 'eacute', 'ecircumflex', 'edieresis', 'igrave', 'iacute', 'icircumflex', 'idieresis', 'ntilde', 'ograve', 'oacute', 'ocircumflex', 'otilde', 'odieresis', 'oslash', 'oe', 'ugrave', 'uacute', 'ucircumflex', 'udieresis', 'yacute', 'ydieresis', 'amacron', 'abreve', 'aogonek', 'aringacute', 'adblgrave', 'ainvertedbreve', 'adotbelow', 'ahookabove', 'acircumflexacute', 'acircumflexgrave', 'acircumflexhookabove', 'acircumflextilde', 'acircumflexdotbelow', 'abreveacute', 'abrevegrave', 'abrevehookabove', 'abrevetilde', 'abrevedotbelow', 'cacute', 'ccircumflex', 'cdotaccent', 'ccaron', 'dcaron', 'emacron', 'ebreve', 'edotaccent', 'eogonek', 'ecaron', 'edblgrave', 'einvertedbreve', 'edotbelow', 'ehookabove', 'etilde', 'ecircumflexacute', 'ecircumflexgrave', 'ecircumflexhookabove', 'ecircumflextilde', 'ecircumflexdotbelow', 'gcircumflex', 'gbreve', 'gdotaccent', 'gcommaaccent', 'gcaron', 'hcircumflex', 'itilde', 'imacron', 'ibreve', 'iogonek',               'idblgrave', 'iinvertedbreve', 'ihookabove', 'idotbelow', 'jcircumflex', 'kcommaaccent', 'lacute', 'lcommaaccent', 'lcaron', 'nacute', 'ncommaaccent', 'ncaron', 'omacron', 'obreve', 'ohungarumlaut', 'ohorn', 'oogonek', 'odblgrave', 'oinvertedbreve', 'odieresismacron', 'otildemacron', 'odotaccentmacron', 'odotbelow', 'ohookabove', 'ocircumflexacute', 'ocircumflexgrave', 'ocircumflexhookabove', 'ocircumflextilde', 'ocircumflexdotbelow', 'ohornacute', 'ohorngrave', 'ohornhookabove', 'ohorntilde', 'ohorndotbelow', 'racute', 'rcommaaccent', 'rcaron', 'rdblgrave', 'rinvertedbreve', 'sacute', 'scircumflex', 'scedilla', 'scaron', 'scommaaccent', 'tcedilla', 'tcaron', 'tcommaaccent', 'utilde', 'umacron', 'ubreve', 'uring', 'uhungarumlaut', 'uogonek', 'uhorn', 'udblgrave', 'uinvertedbreve', 'udotbelow', 'uhookabove', 'uhornacute', 'uhorngrave', 'uhornhookabove', 'uhorntilde', 'uhorndotbelow', 'wcircumflex', 'wgrave', 'wacute', 'wdieresis', 'ycircumflex', 'ymacron', 'ygrave', 'ydotbelow', 'yhookabove', 'ytilde', 'zacute', 'zdotaccent', 'zcaron', 'aeacute', 'oslashacute', 'tbar' ]

def lookYShiftValues(accents):

    yShiftValues = []
    shiftDict = {}
    accentsToShiftDict = {}
    for glyph in accents:
    
        if len(font[glyph].components) > 1:
        
            char = font[glyph].name
            accent = font[glyph].components[-1]
            yShift = accent.offset[1]
        
            yShiftValues.append(yShift)
        
            if yShift in shiftDict.keys():
            
                shiftDict[yShift] = shiftDict[yShift] + [char] + [accent.baseGlyph]
                accentsToShiftDict[yShift] = [accent.baseGlyph] + shiftDict[yShift]
            
            else:
                shiftDict[yShift] = [char] + [accent.baseGlyph]
    return accentsToShiftDict

#look for UC y shift values
yShiftUC = lookYShiftValues(UCaccents)

#look for lc y shift values
#yShiftlc = lookYShiftValues(lcaccents)

#these values will be shifted
for shift, chars in yShiftUC.items():
    
    print ( str(shift) + ": " + str(chars[0]) )
    
    #font[chars].prepareUndo("Shift y value")
    #font[chars].moveBy ( (0.0,shift ) )
    #font[chars].performUndo()
    

    
    
    
    