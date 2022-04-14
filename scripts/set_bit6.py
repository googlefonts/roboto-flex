import os
from fontTools.ttLib import TTFont


CWD = os.path.dirname(__file__)


def set_overlap_flag(varfont):
    glyf = varfont["glyf"]
    for glyph_name in glyf.keys():
        glyph = glyf[glyph_name]
        if glyph.isComposite():
            # Set OVERLAP_COMPOUND bit for compound glyphs
            glyph.components[0].flags |= 0x400
        elif glyph.numberOfContours > 0:
            # Set OVERLAP_SIMPLE bit for simple glyphs
            glyph.flags[0] |= 0x40


def main():
    font_path = os.path.join(CWD, "..", "fonts", "variable", "RobotoFlex[GRAD,XOPQ,XTRA,YOPQ,YTAS,YTDE,YTFI,YTLC,YTUC,opsz,slnt,wdth,wght].ttf")
    ttFont = TTFont(font_path)
    set_overlap_flag(ttFont)
    print("Glyph bits set!")
    ttFont.save(ttFont.reader.file.name)


if __name__ == "__main__":
    main()
