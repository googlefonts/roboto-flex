
size('A1Landscape')

print((width(), height()))

font("RobotoFlex")

for axis, data in listFontVariations().items():
    print((axis, data))
# pick a variation from the current font

#default
fontVariations(wght=400, wdth=100, opsz=14)
txt = "abcdefghijklmnoprstuvwxyz"

# enable hyphenation
hyphenation(True)
# set font size
fontSize(144)
# draw text in a box
textBox(txt, (100, 100, 2000, 1500))

#newPage(2384, 1685)

#saveImage("~/Desktop/proof-RobotoFlex/proof-RobotoFlex.pdf")