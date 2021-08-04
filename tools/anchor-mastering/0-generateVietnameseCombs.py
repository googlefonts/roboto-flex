
font = CurrentFont()

vietnamese = { 'circumflexacutecomb', 'circumflexgravecomb', 'circumflexhookabovecomb', 'circumflextildecomb', 'breveacutecomb', 'brevegravecomb','brevehookabovecomb', 'brevetildecomb', }
vietnameseCase = { 'circumflexacutecomb.case', 'circumflexgravecomb.case', 'circumflexhookabovecomb.case', 'circumflextildecomb.case', 'breveacutecomb.case', 'brevegravecomb.case','brevehookabovecomb.case', 'brevetildecomb.case', }

for comb in vietnamese:

    glyph = font.newGlyph(comb, clear=True)
    
    ref = 'a' + comb
    
    glyph.appendGlyph(font[ ref.replace(' ', '').replace('comb', '') ])

    glyph.width = 1024

    glyph.appendAnchor('_top', (512,font.info.xHeight))
    
    #glyph.appendAnchor('top', (512, abs( glyph.topMargin ) ))

    glyph.decompose()
    
    glyph.removeContour(0)
    glyph.removeContour(0)
    
for comb in vietnameseCase:

    glyph = font.newGlyph(comb, clear=True)
    
    ref = 'A' + comb
    
    glyph.appendGlyph(font[ ref.replace(' ', '').replace('comb.case', '') ])

    glyph.width = 1024

    glyph.appendAnchor('top', (512,font.info.capHeight))

    glyph.decompose()
    
    glyph.removeContour(0)
    glyph.removeContour(0)