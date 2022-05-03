from fontParts.world import *

defaultMaster =                ['../sources/1A-drawings/Mains/RobotoFlex_wght400.ufo']

mastersSidebearings =          [
                                '../sources/1A-drawings/Parametric Axes/RobotoFlex_XTRA323.ufo',
                                '../sources/1A-drawings/Parametric Axes/RobotoFlex_XTRA603.ufo',
                                # '../sources/1A-drawings/Parametric Axes/RobotoFlex_XOPQ27.ufo',
                                # '../sources/1A-drawings/Parametric Axes/RobotoFlex_XOPQ175.ufo'
                                ]

mastersWidhts =                [
                                '../sources/1A-drawings/Mains/RobotoFlex_GRAD-200.ufo',
                                '../sources/1A-drawings/Mains/RobotoFlex_GRAD150.ufo',
                                '../sources/1A-drawings/Parametric Axes/RobotoFlex_YOPQ25.ufo',
                                '../sources/1A-drawings/Parametric Axes/RobotoFlex_YOPQ135.ufo',
                                ]
                                
# mastersWidhtsAndSidebearings = [
#                                 '../sources/1A-drawings/Parametric Axes/RobotoFlex_YTUC528.ufo',
#                                 '../sources/1A-drawings/Parametric Axes/RobotoFlex_YTUC760.ufo',
#                                 '../sources/1A-drawings/Parametric Axes/RobotoFlex_YTLC416.ufo',
#                                 '../sources/1A-drawings/Parametric Axes/RobotoFlex_YTLC570.ufo',
#                                 '../sources/1A-drawings/Parametric Axes/RobotoFlex_YTFI560.ufo',
#                                 '../sources/1A-drawings/Parametric Axes/RobotoFlex_YTFI788.ufo',
#                                 '../sources/1A-drawings/Parametric Axes/RobotoFlex_YTDE-98.ufo',
#                                 '../sources/1A-drawings/Parametric Axes/RobotoFlex_YTDE-305.ufo',
#                                 '../sources/1A-drawings/Parametric Axes/RobotoFlex_YTAS649.ufo',
#                                 '../sources/1A-drawings/Parametric Axes/RobotoFlex_YTAS854.ufo',
#                                 ]

mastersWidhtsAndSidebearings = [
                                '../sources/1A-drawings/Mains/RobotoFlex_GRAD-200.ufo',
                                '../sources/1A-drawings/Mains/RobotoFlex_GRAD150.ufo',
                                '../sources/1A-drawings/Parametric Axes/RobotoFlex_YTUC528.ufo',
                                '../sources/1A-drawings/Parametric Axes/RobotoFlex_YTUC760.ufo',
                                '../sources/1A-drawings/Parametric Axes/RobotoFlex_YTLC416.ufo',
                                '../sources/1A-drawings/Parametric Axes/RobotoFlex_YTLC570.ufo',
                                '../sources/1A-drawings/Parametric Axes/RobotoFlex_YTFI560.ufo',
                                '../sources/1A-drawings/Parametric Axes/RobotoFlex_YTFI788.ufo',
                                '../sources/1A-drawings/Parametric Axes/RobotoFlex_YTDE-98.ufo',
                                '../sources/1A-drawings/Parametric Axes/RobotoFlex_YTDE-305.ufo',
                                '../sources/1A-drawings/Parametric Axes/RobotoFlex_YTAS649.ufo',
                                '../sources/1A-drawings/Parametric Axes/RobotoFlex_YTAS854.ufo',
                                ]

def checkWidhtsAndSidebearings():

    for f in mastersWidhts:
    
        f2 = OpenFont( f, showInterface=False)
        #f2 = AllFonts()[1]
    
        f1Name = defaultMaster
        f2Name = f
    
        def printResults(l):
            for i in l:
                print ( '\t\t -', i )
    
        f1k = set( f1.keys() )
        f2k = set( f2.keys() )

        print ( '=====' )
        print ( 'SPACING DIFF: ' + str(f1.info.familyName+' - '+f1.info.styleName) + ' vs ' + str(f2.info.familyName+' - '+f2.info.styleName) )
        gnames = f1.keys() + f2.keys()
        for gname in sorted(gnames):
            results = []
            if not gname in f1 or not gname in f2:
                #print '\t\t - %s not present in both fonts.' % gname
                continue
                
            # if f1[gname].width != f2[gname].width:
            #     diff = abs( f1[gname].width - f2[gname].width )
                
            #     if diff < 10:
            #         f2[gname].width = f1[gname].width
            #         #results.append('setwidth difference: %s' % ( diff ) )
            #     else:
            #         f2[gname].width = f1[gname].width
            #         results.append('setwidth difference: %s' % ( diff ) )
            #     f2.save()
                    
                #results.append('setwidth difference: %s, %s' % (f1[gname].width, f2[gname].width))
            
            if f1[gname].width != f2[gname].width:
                results.append('setwidth difference: %s, %s' % (f1[gname].width, f2[gname].width))
            #     f2[gname].width = f1[gname].width
            #     f2.save()
            # if f1[gname].leftMargin != f2[gname].leftMargin:
            #     results.append('LSB difference: %s, %s' % (f1[gname].leftMargin, f2[gname].leftMargin))
            # #     f2[gname].leftMargin = f1[gname].leftMargin
            # #     f2.save()
            # if f1[gname].rightMargin != f2[gname].rightMargin:
            #     results.append('RSB difference: %s, %s' % (f1[gname].rightMargin, f2[gname].rightMargin))
            # #     f2[gname].rightMargin = f1[gname].rightMargin
            # #     f2.save()
            if results:
                print ( '\t -', gname )
                for r in results:
                    print ( '\t\t -', r )

# Open the default master
f1 = OpenFont(defaultMaster, showInterface=True)
f1 = CurrentFont()

checkWidhtsAndSidebearings()
