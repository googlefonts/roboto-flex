
f1 = CurrentFont()
f2 = AllFonts()[1]
f1Name = f1.info.familyName+' - '+f1.info.styleName
f2Name = f2.info.familyName+' - '+f2.info.styleName

def printResults(l):
    for i in l:
        print ( '\t\t -', i )


f1k = set(f1.keys())
f2k = set(f2.keys())



print ( '=====' )
print ( 'SPACING DIFF:' )
gnames = f1.keys() + f2.keys()
for gname in sorted(gnames):
    results = []
    if not gname in f1 or not gname in f2:
        #print '\t\t - %s not present in both fonts.' % gname
        continue
    if f1[gname].width != f2[gname].width:
        results.append('setwidth difference: %s, %s' % (f1[gname].width, f2[gname].width))
        f2[gname].width = f1[gname].width
    # if f1[gname].leftMargin != f2[gname].leftMargin:
    #     results.append('LSB difference: %s, %s' % (f1[gname].leftMargin, f2[gname].leftMargin))
    # if f1[gname].rightMargin != f2[gname].rightMargin:
    #     results.append('RSB difference: %s, %s' % (f1[gname].rightMargin, f2[gname].rightMargin))
    if results:
        print ( '\t -', gname )
        for r in results:
            print ( '\t\t -', r )
