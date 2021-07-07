# get source and destination fonts
srcFont = AllFonts()[1]
dstFont = CurrentFont()

# iterate over selected glyphs in the source font

selectedGlyphs = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

#selectedGlyphs = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

#selectedGlyphs = ['brevecomb', 'acutecomb', 'tildecomb', 'dblgravecomb', 'macroncomb', 'dotaccentcomb', 'horncomb', 'dieresiscomb', 'ringcomb', 'circumflexcomb', 'breveinvertedcomb', 'gravecomb', 'caroncomb', 'hookabovecomb', 'hungarumlautcomb']

for glyph in selectedGlyphs:
    
    # get the source glyph
    srcGlyph = srcFont[glyph]
        
    # if the glyph doesn't have any anchors, skip it
    if not len(srcGlyph.anchors):
        continue
            
    print( srcFont[glyph].name )
    
    # get the source glyph
    srcGlyph = srcFont[glyph]

    # if the glyph doesn't have any anchors, skip it
    if not len(srcGlyph.anchors):
        continue

    # get the destination glyph
    dstGlyph = dstFont[glyph]
    
    print( srcFont[glyph].anchors )
    
    dstGlyph.clearAnchors()
    # iterate over all anchors in the source glyph
    for anchor in srcGlyph.anchors:

        
        yUC = dstFont.info.capHeight
        
        ylc = dstFont.info.xHeight
        
        # copy anchor to destination glyph
        if anchor.name == 'top':
            dstGlyph.appendAnchor(anchor.name, ( ( dstGlyph.width ) / 2, ylc + 200))
        if anchor.name == '_top':
            dstGlyph.appendAnchor(anchor.name, ( ( dstGlyph.width ) / 2, ylc))
        elif anchor.name == 'bottom':
            dstGlyph.appendAnchor(anchor.name, ( ( dstGlyph.width ) / 2, anchor.y))
        elif anchor.name == 'center':
            dstGlyph.appendAnchor(anchor.name, ( ( dstGlyph.width ) / 2, ylc / 2))
        elif anchor.name == 'ogonek':
            dstGlyph.appendAnchor(anchor.name, ( ( dstGlyph.width - dstGlyph.rightMargin - 10), anchor.y))
        elif anchor.name == 'topright':
            dstGlyph.appendAnchor(anchor.name, ( ( dstGlyph.width - dstGlyph.rightMargin), yUC))
        else:
            dstGlyph.appendAnchor(anchor.name, ( ( anchor.x ) *2, anchor.y))

print('Done!')