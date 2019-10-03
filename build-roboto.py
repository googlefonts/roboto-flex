# License: Apache 2.0

from __future__ import print_function

# from glyphNameFormatter.data import name2unicode_AGD
from mutatorMath.ufo.document import DesignSpaceDocumentWriter, DesignSpaceDocumentReader
from designSpaceDocument import DesignSpaceDocument, SourceDescriptor, InstanceDescriptor, AxisDescriptor, RuleDescriptor
#from fontTools.designspaceLib import DesignSpaceDocument, SourceDescriptor, InstanceDescriptor, AxisDescriptor, RuleDescriptor

from fontmake.font_project import FontProject
from fontTools.varLib import build
from fontTools.varLib.mutator import instantiateVariableFont
from defcon import Font
import shutil
import os

	
def buildDesignSpace(sources, instances, axes):
	# use DesignSpaceDocument because it supports axis labelNames
	doc = DesignSpaceDocument()
	
	for source in sources:
		s = SourceDescriptor()
		s.path = source["path"]
		s.name = source["name"]
		s.copyInfo = source["copyInfo"]
		s.location = source["location"]
		s.familyName = source["familyName"]
		s.styleName = source["styleName"]
		doc.addSource(s)
	
	for instance in instances:
		i = InstanceDescriptor()
		i.location = instance["location"]
		i.familyName = instance["familyName"]
		i.styleName = instance["styleName"]
		doc.addInstance(i)
	
	for axis in axes:
		a = AxisDescriptor()
		a.minimum = axis["minimum"]
		a.maximum = axis["maximum"]
		a.default = axis["default"]
		a.name = axis["name"]
		a.tag = axis["tag"]
		for languageCode, labelName in axis["labelNames"].items():
			a.labelNames[languageCode] = labelName
		a.map = axis["map"]
		doc.addAxis(a)
		
	return doc

def buildGlyphSet(dflt, fonts):
	# fill the glyph set with default glyphs
	for font in fonts:
		for glyph in dflt:
			glyphName = glyph.name
			if glyphName not in font and glyphName not in composites:
				font.insertGlyph(glyph)
				font[glyphName].lib['com.typemytype.robofont.mark'] = [0, 0, 0, 0.25] # dark grey

# def buildComposites(composites, fonts):
# 	# build the composites
# 	for font in fonts:
# 		for glyphName in composites.keys():
# 			font.newGlyph(glyphName)
# 			composite = font[glyphName]
# 			composite.unicode = name2unicode_AGD[glyphName]
			
# 			value = composites[glyphName]
# 			items = value.split("+")
# 			base = items[0]
# 			items = items[1:]
	
# 			component = composite.instantiateComponent()
# 			component.baseGlyph = base
# 			baseGlyph = font[base]
# 			composite.width = baseGlyph.width
# 			composite.appendComponent(component)
	
# 			for item in items:
# 				baseName, anchorName = item.split("@")
# 				component = composite.instantiateComponent()
# 				component.baseGlyph = baseName
# 				anchor = _anchor = None
# 				for a in baseGlyph.anchors:
# 					if a["name"] == anchorName:
# 						anchor = a
# 				for a in font[baseName].anchors:
# 					if a["name"] == "_"+anchorName:
# 						_anchor = a
# 				if anchor and _anchor:
# 					x = anchor["x"] - _anchor["x"]
# 					y = anchor["y"] - _anchor["y"]
# 					component.move((x, y))
# 				composite.appendComponent(component)
# 			composite.lib['com.typemytype.robofont.mark'] = [0, 0, 0, 0.5] # grey

def setGlyphOrder(glyphOrder, fonts):
	# set the glyph order
	for font in fonts:
		font.glyphOrder = glyphOrder

def clearAnchors(fonts):
	# set the glyph order
	for font in fonts:
		for glyph in font:
		    glyph.clearAnchors()

def saveMasters(fonts, master_dir="master_ufo"):
	# save in master_ufo directory
	for font in fonts:
		path = os.path.join(master_dir, os.path.basename(font.path))

		#added this check because the "master_ufo" folder is getting removed at the beginning of this script
		if not os.path.exists(path):
			os.makedirs(path)
		font.save(path)

with open("sources/RobotoExtremo-ascii.enc") as enc:
	glyphOrder = enc.read().splitlines()

# dictionary of glyph construction used to build the composite accents
composites = {
	"Agrave": "A+grave@top",
	"Aacute": "A+acute@top",
	"Acircumflex": "A+circumflex@top",
	"Atilde": "A+tilde@top",
	"Adieresis": "A+dieresis@top",
	"Aring": "A+ring@top",
	"Ccedilla": "C+cedilla@bottom",
	"Egrave": "E+grave@top",
	"Eacute": "E+acute@top",
	"Ecircumflex": "E+circumflex@top",
	"Edieresis": "E+dieresis@top",
	"Igrave": "I+grave@top",
	"Iacute": "I+acute@top",
	"Icircumflex": "I+circumflex@top",
	"Idieresis": "I+dieresis@top",
	"Ntilde": "N+tilde@top",
	"Ograve": "O+grave@top",
	"Oacute": "O+acute@top",
	"Ocircumflex": "O+circumflex@top",
	"Otilde": "O+tilde@top",
	"Odieresis": "O+dieresis@top",
	"Ugrave": "U+grave@top",
	"Uacute": "U+acute@top",
	"Ucircumflex": "U+circumflex@top",
	"Udieresis": "U+dieresis@top",
	"Yacute": "Y+acute@top",
	"agrave": "a+grave@top",
	"aacute": "a+acute@top",
	"acircumflex": "a+circumflex@top",
	"atilde": "a+tilde@top",
	"adieresis": "a+dieresis@top",
	"aring": "a+ring@top",
	"ccedilla": "c+cedilla@bottom",
	"egrave": "e+grave@top",
	"eacute": "e+acute@top",
	"ecircumflex": "e+circumflex@top",
	"edieresis": "e+dieresis@top",
	"igrave": "dotlessi+grave@top",
	"iacute": "dotlessi+acute@top",
	"icircumflex": "dotlessi+circumflex@top",
	"idieresis": "dotlessi+dieresis@top",
	"ntilde": "n+tilde@top",
	"ograve": "o+grave@top",
	"oacute": "o+acute@top",
	"ocircumflex": "o+circumflex@top",
	"otilde": "o+tilde@top",
	"odieresis": "o+dieresis@top",
	"ugrave": "u+grave@top",
	"uacute": "u+acute@top",
	"ucircumflex": "u+circumflex@top",
	"udieresis": "u+dieresis@top",
	"yacute": "y+acute@top",
	"ydieresis": "y+dieresis@top",
}

print ("Cleaning up...")

# clean up previous build
if os.path.exists("instances"):
	shutil.rmtree("instances", ignore_errors=True)
if os.path.exists("master_ttf"):
	shutil.rmtree("master_ttf", ignore_errors=True)
if os.path.exists("master_ufo"):
	shutil.rmtree("master_ufo", ignore_errors=True)
if os.path.exists("master_ttf_interpolatable"):
	shutil.rmtree("master_ttf_interpolatable", ignore_errors=True)



src_dir = "sources/1-drawings"
master_dir = "master_ufo"
instance_dir = "instances"

# use a temporary designspace to build instances with mutator math
familyName = "RobotoExtremo"
tmpDesignSpace = "tmp.designspace"
doc = DesignSpaceDocumentWriter(tmpDesignSpace)
# sources
doc.addSource(path="sources/1-drawings/RobotoExtremo-Regular.ufo", name="RobotoExtremo-Regular.ufo", location=dict(wght=0, wdth=0, opsz=0), styleName="Regular", familyName=familyName, copyLib=False, copyGroups=False, copyInfo=False, copyFeatures=False, muteKerning=False, muteInfo=False, mutedGlyphNames=None)
# doc.addSource(path="sources/1-drawings/RobotoExtremo-XOPQmin-YOPQmin.ufo", name="RobotoExtremo-XOPQmin-YOPQmin.ufo", location=dict(XYOPQ=-1), styleName="XOPQmin-YOPQmin", familyName=familyName, copyLib=False, copyGroups=False, copyInfo=False, copyFeatures=False, muteKerning=False, muteInfo=False, mutedGlyphNames=None)
# doc.addSource(path="sources/1-drawings/RobotoExtremo-XOPQmax-YOPQmax.ufo", name="RobotoExtremo-XOPQmax-YOPQmax.ufo", location=dict(XYOPQ=1), styleName="XOPQmax-YOPQmax", familyName=familyName, copyLib=False, copyGroups=False, copyInfo=False, copyFeatures=False, muteKerning=False, muteInfo=False, mutedGlyphNames=None)
# doc.addSource(path="sources/1-drawings/RobotoExtremo-XTRAmin.ufo", name="RobotoExtremo-XTRAmin.ufo", location=dict(XTRA=-1), styleName="XTRAmin", familyName=familyName, copyLib=False, copyGroups=False, copyInfo=False, copyFeatures=False, muteKerning=False, muteInfo=False, mutedGlyphNames=None)
# doc.addSource(path="sources/1-drawings/RobotoExtremo-XTRAmax.ufo", name="RobotoExtremo-XTRAmax.ufo", location=dict(XTRA=1), styleName="XTRAmax", familyName=familyName, copyLib=False, copyGroups=False, copyInfo=False, copyFeatures=False, muteKerning=False, muteInfo=False, mutedGlyphNames=None)
# doc.addSource(path="sources/1-drawings/RobotoExtremo-YTLCmin.ufo", name="RobotoExtremo-YTLCmin.ufo", location=dict(YTLC=-1), styleName="YTLCmin", familyName=familyName, copyLib=False, copyGroups=False, copyInfo=False, copyFeatures=False, muteKerning=False, muteInfo=False, mutedGlyphNames=None)
# doc.addSource(path="sources/1-drawings/RobotoExtremo-YTLCmax.ufo", name="RobotoExtremo-YTLCmax.ufo", location=dict(YTLC=1), styleName="YTLCmax", familyName=familyName, copyLib=False, copyGroups=False, copyInfo=False, copyFeatures=False, muteKerning=False, muteInfo=False, mutedGlyphNames=None)
# doc.addSource(path="sources/1-drawings/RobotoExtremo-YTUCmin.ufo", name="RobotoExtremo-YTUCmin.ufo", location=dict(YTUC=-1), styleName="YTUCmin", familyName=familyName, copyLib=False, copyGroups=False, copyInfo=False, copyFeatures=False, muteKerning=False, muteInfo=False, mutedGlyphNames=None)
# doc.addSource(path="sources/1-drawings/RobotoExtremo-YTUCmax.ufo", name="RobotoExtremo-YTUCmax.ufo", location=dict(YTUC=1), styleName="YTUCmax", familyName=familyName, copyLib=False, copyGroups=False, copyInfo=False, copyFeatures=False, muteKerning=False, muteInfo=False, mutedGlyphNames=None)
# doc.addSource(path="sources/1-drawings/RobotoExtremo-YTASmin.ufo", name="RobotoExtremo-YTASmin.ufo", location=dict(YTAS=-1), styleName="YTASmin", familyName=familyName, copyLib=False, copyGroups=False, copyInfo=False, copyFeatures=False, muteKerning=False, muteInfo=False, mutedGlyphNames=None)
# doc.addSource(path="sources/1-drawings/RobotoExtremo-YTASmax.ufo", name="RobotoExtremo-YTASmax.ufo", location=dict(YTAS=1), styleName="YTASmax", familyName=familyName, copyLib=False, copyGroups=False, copyInfo=False, copyFeatures=False, muteKerning=False, muteInfo=False, mutedGlyphNames=None)
# doc.addSource(path="sources/1-drawings/RobotoExtremo-YTDEmin.ufo", name="RobotoExtremo-YTDEmin.ufo", location=dict(YTDE=-1), styleName="YTDEmin", familyName=familyName, copyLib=False, copyGroups=False, copyInfo=False, copyFeatures=False, muteKerning=False, muteInfo=False, mutedGlyphNames=None)
# doc.addSource(path="sources/1-drawings/RobotoExtremo-YTDEmax.ufo", name="RobotoExtremo-YTDEmax.ufo", location=dict(YTDE=1), styleName="YTDEmax", familyName=familyName, copyLib=False, copyGroups=False, copyInfo=False, copyFeatures=False, muteKerning=False, muteInfo=False, mutedGlyphNames=None)

# axes
doc.addAxis(tag="wght", name="wght", minimum=100, maximum=900, default=400, warpMap=None)
doc.addAxis(tag="wdth", name="wdth", minimum=75, maximum=125, default=100, warpMap=None)
doc.addAxis(tag="opsz", name="opsz", minimum=8, maximum=144, default=14, warpMap=None)






# instances
instances = [
#	dict(fileName="instances/RobotoExtremo-opszmax-wghtmin-wdthmax.ufo", location=dict(wght=100, wdth=125, opsz=144), styleName="opszmax-wghtmin-wdthmax", familyName=familyName, postScriptFontName=None, styleMapFamilyName=None, styleMapStyleName=None),
#	dict(fileName="instances/RobotoExtremo-opszmax-wghtmin-wdth075.ufo", location=dict(wght=100, wdth=87, opsz=144), styleName="opszmax-wghtmin-wdth075", familyName=familyName, postScriptFontName=None, styleMapFamilyName=None, styleMapStyleName=None),
#	dict(fileName="instances/RobotoExtremo-opszmax-wghtmin-wdthmin.ufo", location=dict(wght=100, wdth=75, opsz=144), styleName="opszmax-wghtmin-wdthmin", familyName=familyName, postScriptFontName=None, styleMapFamilyName=None, styleMapStyleName=None),
	
#	dict(fileName="instances/RobotoExtremo-opszmax-wghtmax-wdthmax.ufo", location=dict(wght=900, wdth=125, opsz=144), styleName="opszmax-wghtmax-wdthmax", familyName=familyName, postScriptFontName=None, styleMapFamilyName=None, styleMapStyleName=None),
#	dict(fileName="instances/RobotoExtremo-opszmax-wghtmax-wdth075.ufo", location=dict(wght=900, wdth=76, opsz=144), styleName="opszmax-wghtmax-wdth075", familyName=familyName, postScriptFontName=None, styleMapFamilyName=None, styleMapStyleName=None),
#	dict(fileName="instances/RobotoExtremo-opszmax-wghtmax-wdthmin.ufo", location=dict(wght=900, wdth=75, opsz=144), styleName="opszmax-wghtmax-wdthmin", familyName=familyName, postScriptFontName=None, styleMapFamilyName=None, styleMapStyleName=None),
	
#	dict(fileName="instances/RobotoExtremo-opszmax-wdthmax.ufo", location=dict(wght=400, wdth=125, opsz=144), styleName="opszmax-wdthmax", familyName=familyName, postScriptFontName=None, styleMapFamilyName=None, styleMapStyleName=None),
#	dict(fileName="instances/RobotoExtremo-opszmax-wdth075.ufo", location=dict(wght=400, wdth=80, opsz=144), styleName="opszmax-wdth075", familyName=familyName, postScriptFontName=None, styleMapFamilyName=None, styleMapStyleName=None),
#	dict(fileName="instances/RobotoExtremo-opszmax-wdthmin.ufo", location=dict(wght=400, wdth=75, opsz=144), styleName="opszmax-wdthmin", familyName=familyName, postScriptFontName=None, styleMapFamilyName=None, styleMapStyleName=None),
]
for instance in instances:
	doc.startInstance(**instance)
	doc.writeInfo()
	doc.writeKerning()
	doc.endInstance()

doc.save()
# read and process the designspace
doc = DesignSpaceDocumentReader(tmpDesignSpace, ufoVersion=2, roundGeometry=False, verbose=False)
print ("Reading DesignSpace...")
doc.process(makeGlyphs=True, makeKerning=True, makeInfo=True)
os.remove(tmpDesignSpace) # clean up

# update the instances with the source fonts
# print str(instances) + ' instances! '
for instance in instances:
	fileName = os.path.basename(instance["fileName"])
	source_path = os.path.join(src_dir, fileName)
	instance_path = os.path.join(instance_dir, fileName)
	source_font = Font(source_path)
	instance_font = Font(instance_path)
	# insert the source glyphs in the instance font
	for glyph in source_font:
		instance_font.insertGlyph(glyph)
	master_path = os.path.join(master_dir, fileName)
	instance_font.save(master_path)

designSpace = "sources/RobotoExtremo.designspace"
sources = [
	dict(path="master_ufo/RobotoExtremo-Regular.ufo", name="RobotoExtremo-Regular.ufo", location=dict( wght=400, wdth=100, opsz=14, GRAD=0), styleName="Regular", familyName=familyName, copyInfo=True),
# 	# backup
# 	dict(path="master_ufo/RobotoExtremo-Regular.ufo", name="RobotoExtremo-Regular.ufo", location=dict(XOPQ=94, YOPQ=77, XTRA=359, YTLC=514, YTUC=712, YTAS=750, YTDE=-203, YTAD=563, YTDD=0, UDLN=-49, wght=400, wdth=100, opsz=12, PWGT=94, PWDT=712, POPS=0, GRAD=0, YTRA=0), styleName="Regular", familyName=familyName, copyInfo=True),
	
 	dict(path="master_ufo/RobotoExtremo-XTRAmin.ufo", name="RobotoExtremo-XTRAmin.ufo", location=dict(XTRA=323), styleName="XTRAmin", familyName=familyName, copyInfo=False),
 	dict(path="master_ufo/RobotoExtremo-XTRAmax.ufo", name="RobotoExtremo-XTRAmax.ufo", location=dict(XTRA=603), styleName="XTRAmax", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-XOPQmin.ufo", name="RobotoExtremo-XOPQmin.ufo", location=dict(XOPQ=27), styleName="XOPQmin", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-XOPQmax.ufo", name="RobotoExtremo-XOPQmax.ufo", location=dict(XOPQ=175), styleName="XOPQmax", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-YOPQmin.ufo", name="RobotoExtremo-YOPQmin.ufo", location=dict(YOPQ=25), styleName="YOPQmin", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-YOPQmax.ufo", name="RobotoExtremo-YOPQmax.ufo", location=dict(YOPQ=135), styleName="YOPQmax", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-XOPQmin-YOPQmin.ufo", name="RobotoExtremo-XOPQmin-YOPQmin.ufo", location=dict(XOPQ=26, YOPQ=26), styleName="XOPQmin-YOPQmin", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-XOPQmax-YOPQmax.ufo", name="RobotoExtremo-XOPQmax-YOPQmax.ufo", location=dict(XOPQ=171, YOPQ=132), styleName="XOPQmax-YOPQmax", familyName=familyName, copyInfo=False),

# 	dict(path="master_ufo/RobotoExtremo-XOPQmin-YOPQmin-XTRAmin.ufo", name="RobotoExtremo-XOPQmin-YOPQmin-XTRAmin.ufo", location=dict(XOPQ=26, YOPQ=26, XTRA=210), styleName="XOPQmin-YOPQmin-XTRAmin", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-XOPQmin-YOPQmin-XTRAmax.ufo", name="RobotoExtremo-XOPQmin-YOPQmin-XTRAmax.ufo", location=dict(XOPQ=26, YOPQ=26, XTRA=513), styleName="XOPQmin-YOPQmin-XTRAmin", familyName=familyName, copyInfo=False),
	
# 	dict(path="master_ufo/RobotoExtremo-YOLCmin.ufo", name="RobotoExtremo-YOLCmin.ufo", location=dict(YOLC=25), styleName="YOLCmin", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-YOLCmax.ufo", name="RobotoExtremo-YOLCmax.ufo", location=dict(YOLC=130), styleName="YOLCmax", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-YOUCmin.ufo", name="RobotoExtremo-YOUCmin.ufo", location=dict(YOUC=25), styleName="YOUCmin", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-YOUCmax.ufo", name="RobotoExtremo-YOUCmax.ufo", location=dict(YOUC=135), styleName="YOUCmax", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-YOFImin.ufo", name="RobotoExtremo-YOFImin.ufo", location=dict(YOFI=25), styleName="YOFImin", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-YOFImax.ufo", name="RobotoExtremo-YOFImax.ufo", location=dict(YOFI=150), styleName="YOFImax", familyName=familyName, copyInfo=False),
# 	
# 	dict(path="master_ufo/RobotoExtremo-YTLCmin.ufo", name="RobotoExtremo-YTLCmin.ufo", location=dict(YTLC=416), styleName="YTLCmin", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-YTLCmax.ufo", name="RobotoExtremo-YTLCmax.ufo", location=dict(YTLC=570), styleName="YTLCmax", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-YTUCmin.ufo", name="RobotoExtremo-YTUCmin.ufo", location=dict(YTUC=528), styleName="YTUCmin", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-YTUCmax.ufo", name="RobotoExtremo-YTUCmax.ufo", location=dict(YTUC=760), styleName="YTUCmax", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-YTASmin.ufo", name="RobotoExtremo-YTASmin.ufo", location=dict(YTAS=649), styleName="YTASmin", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-YTASmax.ufo", name="RobotoExtremo-YTASmax.ufo", location=dict(YTAS=854), styleName="YTASmax", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-YTDEmin.ufo", name="RobotoExtremo-YTDEmin.ufo", location=dict(YTDE=-305), styleName="YTDEmin", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-YTDEmax.ufo", name="RobotoExtremo-YTDEmax.ufo", location=dict(YTDE=-98), styleName="YTDEmax", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-YTFImin.ufo", name="RobotoExtremo-YTFImin.ufo", location=dict(YTFI=560), styleName="YTFImin", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-YTFImax.ufo", name="RobotoExtremo-YTFImax.ufo", location=dict(YTFI=788), styleName="YTFImax", familyName=familyName, copyInfo=False),
# 	
# 	dict(path="master_ufo/RobotoExtremo-XOLCmin.ufo", name="RobotoExtremo-XOLCmin.ufo", location=dict(XOLC=27), styleName="XOLCmin", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-XOLCmax.ufo", name="RobotoExtremo-XOLCmax.ufo", location=dict(XOLC=170), styleName="XOLCmax", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-XOUCmin.ufo", name="RobotoExtremo-XOUCmin.ufo", location=dict(XOUC=27), styleName="XOUCmin", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-XOUCmax.ufo", name="RobotoExtremo-XOUCmax.ufo", location=dict(XOUC=170), styleName="XOUCmax", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-XOFImin.ufo", name="RobotoExtremo-XOFImin.ufo", location=dict(XOFI=27), styleName="XOFImin", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-XOFImax.ufo", name="RobotoExtremo-XOFImax.ufo", location=dict(XOFI=180), styleName="XOFImax", familyName=familyName, copyInfo=False),
# 	
# 	dict(path="master_ufo/RobotoExtremo-XTLCmin.ufo", name="RobotoExtremo-XTLCmin.ufo", location=dict(XTLC=129), styleName="XTLCmin", familyName=familyName, copyInfo=False),
#  	dict(path="master_ufo/RobotoExtremo-XTLCmax.ufo", name="RobotoExtremo-XTLCmax.ufo", location=dict(XTLC=393), styleName="XTLCmax", familyName=familyName, copyInfo=False),
#  	dict(path="master_ufo/RobotoExtremo-XTUCmin.ufo", name="RobotoExtremo-XTUCmin.ufo", location=dict(XTUC=227), styleName="XTUCmin", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-XTUCmax.ufo", name="RobotoExtremo-XTUCmax.ufo", location=dict(XTUC=507), styleName="XTUCmax", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-XTFImin.ufo", name="RobotoExtremo-XTFImin.ufo", location=dict(XTFI=155), styleName="XTFImin", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-XTFImax.ufo", name="RobotoExtremo-XTFImax.ufo", location=dict(XTFI=392), styleName="XTFImax", familyName=familyName, copyInfo=False),
 	
# 	dict(path="master_ufo/RobotoExtremo-YTADmin.ufo", name="RobotoExtremo-YTADmin.ufo", location=dict(YTAD=460), styleName="YTADmin", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-YTADmax.ufo", name="RobotoExtremo-YTADmax.ufo", location=dict(YTAD=600), styleName="YTADmax", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-YTDDmin.ufo", name="RobotoExtremo-YTDDmin.ufo", location=dict(YTDD=-1), styleName="YTDDmin", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-YTDDmax.ufo", name="RobotoExtremo-YTDDmax.ufo", location=dict(YTDD=1), styleName="YTDDmax", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-UDLNmin.ufo", name="RobotoExtremo-UDLNmin.ufo", location=dict(UDLN=-195), styleName="UDLNmin", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-UDLNmax.ufo", name="RobotoExtremo-UDLNmax.ufo", location=dict(UDLN=0), styleName="UDLNmax", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-YTRAmin.ufo", name="RobotoExtremo-YTRAmin.ufo", location=dict(YTRA=-1), styleName="YTRAmin", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-YTRAmax.ufo", name="RobotoExtremo-YTRAmax.ufo", location=dict(YTRA=1), styleName="YTRAmax", familyName=familyName, copyInfo=False),

	dict(path="master_ufo/RobotoExtremo-GRADmin.ufo", name="RobotoExtremo-GRADmin.ufo", location=dict(GRAD=-1), styleName="GRADmin", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-GRADmax.ufo", name="RobotoExtremo-GRADmax.ufo", location=dict(GRAD=1), styleName="GRADmax", familyName=familyName, copyInfo=False),
		
	dict(path="master_ufo/RobotoExtremo-wghtmin.ufo", name="RobotoExtremo-wghtmin.ufo", location=dict(wght=100), styleName="wghtmin", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-wghtmax.ufo", name="RobotoExtremo-wghtmax.ufo", location=dict(wght=900), styleName="wghtmax", familyName=familyName, copyInfo=False),


# 	dict(path="master_ufo/RobotoExtremo-wghtmin.ufo", name="RobotoExtremo-wghtmin.ufo", location=dict(PWGT=44), styleName="wghtmin", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-wghtmax.ufo", name="RobotoExtremo-wghtmax.ufo", location=dict(PWGT=150), styleName="wghtmax", familyName=familyName, copyInfo=False),
	
	dict(path="master_ufo/RobotoExtremo-opszmin.ufo", name="RobotoExtremo-opszmin.ufo", location=dict(opsz=8), styleName="opszmin", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-opsz36.ufo", name="RobotoExtremo-opsz36.ufo", location=dict(opsz=36), styleName="opsz36", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opszmax.ufo", name="RobotoExtremo-opszmax.ufo", location=dict(opsz=144), styleName="opszmax", familyName=familyName, copyInfo=False),

	dict(path="master_ufo/RobotoExtremo-wdthmin.ufo", name="RobotoExtremo-wdthmin.ufo", location=dict(wdth=25), styleName="wdthmin", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-wdthmax.ufo", name="RobotoExtremo-wdthmax.ufo", location=dict(wdth=151), styleName="wdthmax", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-wdthmin.ufo", name="RobotoExtremo-wdthmin.ufo", location=dict(PWDT=560), styleName="wdthmin", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-wdthmax.ufo", name="RobotoExtremo-wdthmax.ufo", location=dict(PWDT=867), styleName="wdthmax", familyName=familyName, copyInfo=False),
	
	
	dict(path="master_ufo/RobotoExtremo-opszmax-wdthmax.ufo", name="RobotoExtremo-opszmax-wdthmax.ufo", location=dict(wdth=151, opsz=144), styleName="opszmax-wdthmax", familyName=familyName, copyInfo=False),
#	dict(path="master_ufo/RobotoExtremo-opszmax-wdth075.ufo", name="RobotoExtremo-opszmax-wdth075.ufo", location=dict(wdth=80, opsz=144), styleName="opszmax-wdthmin075", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opszmax-wdthmin.ufo", name="RobotoExtremo-opszmax-wdthmin.ufo", location=dict(wdth=25, opsz=144), styleName="opszmax-wdthmin", familyName=familyName, copyInfo=False),
	
	dict(path="master_ufo/RobotoExtremo-opszmax-wghtmax.ufo", name="RobotoExtremo-opszmax-wghtmax.ufo", location=dict(wght=900, opsz=144), styleName="opszmax-wghtmax", familyName=familyName, copyInfo=False),
#	dict(path="master_ufo/RobotoExtremo-opszmax-wght780.ufo", name="RobotoExtremo-opszmax-wght780.ufo", location=dict(wght=780, opsz=144), styleName="opszmax-wght780", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opszmax-wghtmin.ufo", name="RobotoExtremo-opszmax-wghtmin.ufo", location=dict(wght=100, opsz=144), styleName="opszmax-wghtmin", familyName=familyName, copyInfo=False),
	
	dict(path="master_ufo/RobotoExtremo-opszmax-wghtmin-wdthmax.ufo", name="RobotoExtremo-opszmax-wghtmin-wdthmax.ufo", location=dict(wght=100, wdth=151, opsz=144), styleName="opszmax-wghtmin-wdthmax", familyName=familyName, copyInfo=False),
#	dict(path="master_ufo/RobotoExtremo-opszmax-wghtmin-wdth075.ufo", name="RobotoExtremo-opszmax-wghtmin-wdth075.ufo", location=dict(wght=100, wdth=87, opsz=144), styleName="opszmax-wghtmin-wdth075", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opszmax-wghtmin-wdthmin.ufo", name="RobotoExtremo-opszmax-wghtmin-wdthmin.ufo", location=dict(wght=100, wdth=25, opsz=144), styleName="opszmax-wghtmin-wdthmin", familyName=familyName, copyInfo=False),
	
 	dict(path="master_ufo/RobotoExtremo-opszmax-wghtmax-wdthmax.ufo", name="RobotoExtremo-opszmax-wghtmax-wdthmax.ufo", location=dict(wght=900, opsz=144, wdth=151), styleName="opszmax-wghtmax-wdthmax", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-opszmax-wghtmax-wdth075.ufo", name="RobotoExtremo-opszmax-wghtmax-wdth075.ufo", location=dict(wght=900, opsz=144, wdth=76), styleName="opszmax-wghtmax-wdth075", familyName=familyName, copyInfo=False),
 	dict(path="master_ufo/RobotoExtremo-opszmax-wghtmax-wdthmin.ufo", name="RobotoExtremo-opszmax-wghtmax-wdthmin.ufo", location=dict(wght=900, opsz=144, wdth=25), styleName="opszmax-wghtmax-wdthmin", familyName=familyName, copyInfo=False),


	dict(path="master_ufo/RobotoExtremo-opszmin-wdthmax.ufo", name="RobotoExtremo-opszmin-wdthmax.ufo", location=dict(wdth=151, opsz=8), styleName="opszmin-wdthmax", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opszmin-wdthmin.ufo", name="RobotoExtremo-opszmin-wdthmin.ufo", location=dict(wdth=25, opsz=8), styleName="opszmin-wdthmin", familyName=familyName, copyInfo=False),
	
	dict(path="master_ufo/RobotoExtremo-opszmin-wghtmax.ufo", name="RobotoExtremo-opszmin-wghtmax.ufo", location=dict(wght=900, opsz=8), styleName="opszmin-wghtmax", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opszmin-wghtmin.ufo", name="RobotoExtremo-opszmin-wghtmin.ufo", location=dict(wght=100, opsz=8), styleName="opszmin-wghtmin", familyName=familyName, copyInfo=False),

## Leveling intermediates
# 	dict(path="master_ufo/RobotoExtremo-opsz14wght900.ufo", name="RobotoExtremo-opsz14wght900.ufo", location=dict(wght=900, opsz=14), styleName="opsz14wght900", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-opsz18wght900.ufo", name="RobotoExtremo-opsz18wght900.ufo", location=dict(wght=900, opsz=18), styleName="opsz18wght900", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-opsz24wght100.ufo", name="RobotoExtremo-opsz24wght100.ufo", location=dict(wght=100, opsz=24), styleName="opsz24wght100", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-opsz24wght900.ufo", name="RobotoExtremo-opsz24wght900.ufo", location=dict(wght=900, opsz=24), styleName="opsz24wght900", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-opsz36wght100.ufo", name="RobotoExtremo-opsz36wght100.ufo", location=dict(wght=100, opsz=36), styleName="opsz36wght100", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-opsz36wght700.ufo", name="RobotoExtremo-opsz36wght700.ufo", location=dict(wght=700, opsz=36), styleName="opsz36wght900", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-opsz36wght900.ufo", name="RobotoExtremo-opsz36wght900.ufo", location=dict(wght=900, opsz=36), styleName="opsz36wght900", familyName=familyName, copyInfo=False),

## Figures
	dict(path="master_ufo/RobotoExtremo-opsz18wghtminwdthmin.ufo", name="RobotoExtremo-opsz18wghtminwdthmin.ufo", location=dict(wght=100, opsz=18, wdth=25), styleName="opsz18wghtminwdthmin", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz24wghtminwdthmin.ufo", name="RobotoExtremo-opsz24wghtminwdthmin.ufo", location=dict(wght=100, opsz=24, wdth=25), styleName="opsz24wghtminwdthmin", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz36wght100wdthmin.ufo", name="RobotoExtremo-opsz36wght100wdthmin.ufo", location=dict(wght=100, opsz=36, wdth=25), styleName="opsz36wght100wdthmin", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz36wght600wdthmin.ufo", name="RobotoExtremo-opsz36wght600wdthmin.ufo", location=dict(wght=600, opsz=36, wdth=25), styleName="opsz36wght600wdthmin", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz18wght700wdthmin.ufo", name="RobotoExtremo-opsz18wght700wdthmin.ufo", location=dict(wght=700, opsz=18, wdth=25), styleName="opsz18wght700wdthmin", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz24wght700wdthmin.ufo", name="RobotoExtremo-opsz24wght700wdthmin.ufo", location=dict(wght=700, opsz=24, wdth=25), styleName="opsz24wght700wdthmin", familyName=familyName, copyInfo=False),
	
	dict(path="master_ufo/RobotoExtremo-opsz24wght100.ufo", name="RobotoExtremo-opsz24wght100.ufo", location=dict(wght=100, opsz=24), styleName="opsz24wght100", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz36wght100.ufo", name="RobotoExtremo-opsz36wght100.ufo", location=dict(wght=100, opsz=36), styleName="opsz36wght100", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz18wght700.ufo", name="RobotoExtremo-opsz18wght700.ufo", location=dict(wght=700, opsz=18), styleName="opsz18wght700", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz24wght700.ufo", name="RobotoExtremo-opsz24wght700.ufo", location=dict(wght=700, opsz=24), styleName="opsz24wght700", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz36wght700.ufo", name="RobotoExtremo-opsz36wght700.ufo", location=dict(wght=700, opsz=36), styleName="opsz36wght100", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz18wght900.ufo", name="RobotoExtremo-opsz18wght900.ufo", location=dict(wght=900, opsz=18), styleName="opsz18wght900", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz24wght900.ufo", name="RobotoExtremo-opsz24wght900.ufo", location=dict(wght=900, opsz=24), styleName="opsz24wght900", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz36wght900.ufo", name="RobotoExtremo-opsz36wght900.ufo", location=dict(wght=900, opsz=36), styleName="opsz36wght900", familyName=familyName, copyInfo=False),
	
	
	dict(path="master_ufo/RobotoExtremo-opsz24wghtminwdthmax.ufo", name="RobotoExtremo-opsz24wghtminwdthmax.ufo", location=dict(wght=100, opsz=24, wdth=151), styleName="opsz24wghtminwdthmax", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz36wght700wdthmax.ufo", name="RobotoExtremo-opsz36wght700wdthmax.ufo", location=dict(wght=700, opsz=36, wdth=151), styleName="opsz36wght700wdthmax", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz144wght500wdthmax.ufo", name="RobotoExtremo-opsz144wght500wdthmax.ufo", location=dict(wght=500, opsz=144, wdth=151), styleName="opsz144wght500wdthmax", familyName=familyName, copyInfo=False),
	
# #	NEW Caping
	
	dict(path="master_ufo/RobotoExtremo-opszmax-wghtmin-wdthmin-GRADmin.ufo", name="RobotoExtremo-opszmax-wghtmin-wdthmin-GRADmin.ufo", location=dict(wght=100, opsz=144, wdth=25, GRAD=-1), styleName="opszmax-wghtmin-wdthmin-GRADmin", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opszmax-wghtmin-wdthmin-GRADmax.ufo", name="RobotoExtremo-opszmax-wghtmin-wdthmin-GRADmax.ufo", location=dict(wght=100, opsz=144, wdth=25, GRAD=1), styleName="opszmax-wghtmin-wdthmin-GRADmax", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opszmax-wghtmin-wdthmax-GRADmin.ufo", name="RobotoExtremo-opszmax-wghtmin-wdthmax-GRADmin.ufo", location=dict(wght=100, opsz=144, wdth=151, GRAD=-1), styleName="opszmax-wghtmin-wdthmax-GRADmin", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opszmax-wghtmin-wdthmax-GRADmax.ufo", name="RobotoExtremo-opszmax-wghtmin-wdthmax-GRADmax.ufo", location=dict(wght=100, opsz=144, wdth=151, GRAD=1), styleName="opszmax-wghtmin-wdthmax-GRADmax", familyName=familyName, copyInfo=False),
	
	dict(path="master_ufo/RobotoExtremo-opszmax-wghtmin-GRADmax.ufo", name="RobotoExtremo-opszmax-wghtmin-GRADmax.ufo", location=dict(wght=100, opsz=144, GRAD=1), styleName="opszmax-wghtmin-GRADmax", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opszmax-wghtmin-GRADmin.ufo", name="RobotoExtremo-opszmax-wghtmin-GRADmin.ufo", location=dict(wght=100, opsz=144, GRAD=-1), styleName="opszmax-wghtmin-GRADmin", familyName=familyName, copyInfo=False),
		
	
# #	Caping & trimming instances
# #	github issue 36
#  	dict(path="master_ufo/RobotoExtremo-opszmax-wdth100-wghtmax-GRADmax.ufo", name="RobotoExtremo-opszmax-wdth100-wghtmax-GRADmax.ufo", location=dict(wght=900, opsz=144, wdth=100, GRAD=1), styleName="opszmax-wdth100-wghtmax-GRADmax", familyName=familyName, copyInfo=False),
#  	dict(path="master_ufo/RobotoExtremo-opszmax-wdth100-wghtmin-GRADmin.ufo", name="RobotoExtremo-opszmax-wdth100-wghtmin-GRADmin.ufo", location=dict(wght=100, opsz=144, wdth=100, GRAD=-1), styleName="opszmax-wdth100-wghtmin-GRADmin", familyName=familyName, copyInfo=False),
#  	dict(path="master_ufo/RobotoExtremo-opszmax-wdthmin-wght400-XTRAmin.ufo", name="RobotoExtremo-opszmax-wdthmin-wght400-XTRAmin.ufo", location=dict(wght=400, opsz=144, wdth=75, XTRA=227), styleName="opszmax-wdthmin-wght400-XTRAmin", familyName=familyName, copyInfo=False),
#  	dict(path="master_ufo/RobotoExtremo-opszmax-wdthmin-wght900-XTRAmin.ufo", name="RobotoExtremo-opszmax-wdthmin-wght900-XTRAmin.ufo", location=dict(wght=900, opsz=144, wdth=75, XTRA=227), styleName="opszmax-wdthmin-wght900-XTRAmin", familyName=familyName, copyInfo=False),
# 
# #	github issue 40
#  	dict(path="master_ufo/RobotoExtremo-opszmax-wdth100-wghtmax-GRADmax.ufo", name="RobotoExtremo-opszmax-wdth100-wghtmax-GRADmax.ufo", location=dict(wght=900, opsz=144, wdth=100, GRAD=1, YTUC=528), styleName="opszmax-wdth100-wghtmax-GRADmax", familyName=familyName, copyInfo=False),
#  	dict(path="master_ufo/RobotoExtremo-opszmax-wdth100-wghtmax-GRADmax.ufo", name="RobotoExtremo-opszmax-wdth100-wghtmax-GRADmax.ufo", location=dict(wght=900, opsz=144, wdth=100, GRAD=1, YTLC=416), styleName="opszmax-wdth100-wghtmax-GRADmax", familyName=familyName, copyInfo=False),
#  	dict(path="master_ufo/RobotoExtremo-opszmax-wdth100-wghtmax-GRADmax.ufo", name="RobotoExtremo-opszmax-wdth100-wghtmax-GRADmax.ufo", location=dict(wght=900, opsz=144, wdth=100, GRAD=1, YTFI=560), styleName="opszmax-wdth100-wghtmax-GRADmax", familyName=familyName, copyInfo=False),
#  	dict(path="master_ufo/RobotoExtremo-opszmax-wdth100-wghtmax-GRADmax.ufo", name="RobotoExtremo-opszmax-wdth100-wghtmax-GRADmax.ufo", location=dict(wght=900, opsz=144, wdth=100, GRAD=1, YOPQ=25), styleName="opszmax-wdth100-wghtmax-GRADmax", familyName=familyName, copyInfo=False),
#  	dict(path="master_ufo/RobotoExtremo-opszmax-wdth100-wghtmax-GRADmax.ufo", name="RobotoExtremo-opszmax-wdth100-wghtmax-GRADmax.ufo", location=dict(wght=900, opsz=144, wdth=100, GRAD=1, YTDE=-305), styleName="opszmax-wdth100-wghtmax-GRADmax", familyName=familyName, copyInfo=False),
#  	dict(path="master_ufo/RobotoExtremo-opszmax-wdth100-wghtmax-GRADmax.ufo", name="RobotoExtremo-opszmax-wdth100-wghtmax-GRADmax.ufo", location=dict(wght=900, opsz=144, wdth=100, GRAD=1, YTAS=649), styleName="opszmax-wdth100-wghtmax-GRADmax", familyName=familyName, copyInfo=False),
#  	
#  	dict(path="master_ufo/RobotoExtremo-opszmax-wdthmin-wght900-XTRAmin.ufo", name="RobotoExtremo-opszmax-wdthmin-wght900-XTRAmin.ufo", location=dict(wght=900, opsz=144, wdth=100, XTRA=227, YTUC=528), styleName="opszmax-wdth100-wghtmax-XTRAmin", familyName=familyName, copyInfo=False),
#  	dict(path="master_ufo/RobotoExtremo-opszmax-wdthmin-wght900-XTRAmin.ufo", name="RobotoExtremo-opszmax-wdthmin-wght900-XTRAmin.ufo", location=dict(wght=900, opsz=144, wdth=100, XTRA=227, YTLC=416), styleName="opszmax-wdth100-wghtmax-XTRAmin", familyName=familyName, copyInfo=False),
#  	dict(path="master_ufo/RobotoExtremo-opszmax-wdthmin-wght900-XTRAmin.ufo", name="RobotoExtremo-opszmax-wdthmin-wght900-XTRAmin.ufo", location=dict(wght=900, opsz=144, wdth=100, XTRA=227, YTFI=560), styleName="opszmax-wdth100-wghtmax-XTRAmin", familyName=familyName, copyInfo=False),
#  	dict(path="master_ufo/RobotoExtremo-opszmax-wdthmin-wght900-XTRAmin.ufo", name="RobotoExtremo-opszmax-wdthmin-wght900-XTRAmin.ufo", location=dict(wght=900, opsz=144, wdth=100, XTRA=227, YOPQ=25), styleName="opszmax-wdth100-wghtmax-XTRAmin", familyName=familyName, copyInfo=False),
#  	dict(path="master_ufo/RobotoExtremo-opszmax-wdthmin-wght900-XTRAmin.ufo", name="RobotoExtremo-opszmax-wdthmin-wght900-XTRAmin.ufo", location=dict(wght=900, opsz=144, wdth=100, XTRA=227, YTDE=-305), styleName="opszmax-wdth100-wghtmax-XTRAmin", familyName=familyName, copyInfo=False),
#  	dict(path="master_ufo/RobotoExtremo-opszmax-wdthmin-wght900-XTRAmin.ufo", name="RobotoExtremo-opszmax-wdthmin-wght900-XTRAmin.ufo", location=dict(wght=900, opsz=144, wdth=100, XTRA=227, YTAS=649), styleName="opszmax-wdth100-wghtmax-XTRAmin", familyName=familyName, copyInfo=False),
# 
#  	
#  #	41
#  	dict(path="master_ufo/RobotoExtremo-opszmax-wdth100-wghtmmax-YTASmin.ufo", name="RobotoExtremo-opszmax-wdth100-wghtmmax-YTASmin.ufo", location=dict(wght=900, opsz=144, wdth=100, YTAS=649), styleName="opszmax-wdth100-wghtmmax-YTASmin", familyName=familyName, copyInfo=False),
#  	dict(path="master_ufo/RobotoExtremo-opszmax-wdth100-wghtmmax-YTDEmin.ufo", name="RobotoExtremo-opszmax-wdth100-wghtmmax-YTDEmin.ufo", location=dict(wght=900, opsz=144, wdth=100, YTDE=-305), styleName="opszmax-wdth100-wghtmmax-YTDEmin", familyName=familyName, copyInfo=False),

	
	
]
#instances = []
axes = [
	


	dict(minimum=100, maximum=900, default=400, name="wght", tag="wght", labelNames={"en": "wght"}, map=[]),
	dict(minimum=25, maximum=151, default=100, name="wdth", tag="wdth", labelNames={"en": "wdth"}, map=[]),
	dict(minimum=8, maximum=144, default=14, name="opsz", tag="opsz", labelNames={"en": "opsz"}, map=[]),
# 	dict(minimum=44, maximum=150, default=94, name="PWGT", tag="PWGT", labelNames={"en": "PWGT"}, map=[]),
# 	dict(minimum=560, maximum=867, default=712, name="PWDT", tag="PWDT", labelNames={"en": "PWDT"}, map=[]),
# 	dict(minimum=-1, maximum=1, default=0, name="POPS", tag="POPS", labelNames={"en": "POPS"}, map=[]),
	dict(minimum=-1, maximum=1, default=0, name="GRAD", tag="GRAD", labelNames={"en": "GRAD"}, map=[]),
# 	dict(minimum=-1, maximum=1, default=0, name="YTRA", tag="YTRA", labelNames={"en": "YTRA"}, map=[]),
	dict(minimum=323, maximum=603, default=468, name="XTRA", tag="XTRA", labelNames={"en": "XTRA"}, map=[]),
	dict(minimum=27, maximum=175, default=96, name="XOPQ", tag="XOPQ", labelNames={"en": "XOPQ"}, map=[]),
	dict(minimum=25, maximum=135, default=79, name="YOPQ", tag="YOPQ", labelNames={"en": "YOPQ"}, map=[]),

# 	dict(minimum=25, maximum=130, default=71, name="YOLC", tag="YOLC", labelNames={"en": "YOLC"}, map=[]),
#  	dict(minimum=25, maximum=135, default=79, name="YOUC", tag="YOUC", labelNames={"en": "YOUC"}, map=[]),
#  	dict(minimum=25, maximum=150, default=85, name="YOFI", tag="YOFI", labelNames={"en": "YOFI"}, map=[]),
# 	dict(minimum=416, maximum=570, default=514, name="YTLC", tag="YTLC", labelNames={"en": "YTLC"}, map=[]),
# 	dict(minimum=528, maximum=760, default=712, name="YTUC", tag="YTUC", labelNames={"en": "YTUC"}, map=[]),
# 	dict(minimum=649, maximum=854, default=750, name="YTAS", tag="YTAS", labelNames={"en": "YTAS"}, map=[]),
# 	dict(minimum=-305, maximum=-98, default=-203, name="YTDE", tag="YTDE", labelNames={"en": "YTDE"}, map=[]),
# 	dict(minimum=560, maximum=788, default=738, name="YTFI", tag="YTFI", labelNames={"en": "YTFI"}, map=[]),
# 	
# 	
# 	dict(minimum=27, maximum=170, default=93, name="XOLC", tag="XOLC", labelNames={"en": "XOLC"}, map=[]),
# 	dict(minimum=27, maximum=170, default=93, name="XOUC", tag="XOUC", labelNames={"en": "XOUC"}, map=[]),
# 	dict(minimum=27, maximum=180, default=97, name="XOFI", tag="XOFI", labelNames={"en": "XOFI"}, map=[]),
# 	dict(minimum=129, maximum=393, default=240, name="XTLC", tag="XTLC", labelNames={"en": "XTLC"}, map=[]),
# 	dict(minimum=227, maximum=507, default=367, name="XTUC", tag="XTUC", labelNames={"en": "XTUC"}, map=[]),
# 	dict(minimum=155, maximum=392, default=292, name="XTFI", tag="XTFI", labelNames={"en": "XTFI"}, map=[]),
# 	dict(minimum=155, maximum=392, default=292, name="XTFI", tag="XTFI", labelNames={"en": "XTFI"}, map=[]),

# 	dict(minimum=460, maximum=600, default=563, name="YTAD", tag="YTAD", labelNames={"en": "YTAD"}, map=[]),
# 	dict(minimum=-1, maximum=1, default=0, name="YTDD", tag="YTDD", labelNames={"en": "YTDD"}, map=[]),
# 	dict(minimum=-195, maximum=0, default=-49, name="UDLN", tag="UDLN", labelNames={"en": "UDLN"}, map=[]),

]

doc = buildDesignSpace(sources, instances, axes)


#add rule for dollar. Needs to be after doc = buildDesignSpace() because this doc is a DesignSpaceDocument(), rather than the doc above which is a DesignSpaceDocumentReader() object
r1 = RuleDescriptor()
r1.name = "dollar-stroke-wght"
r1.conditions.append(dict(name="wght", minimum=600, maximum=900))
r1.subs.append(("dollar", "dollar.rvrn"))
doc.addRule(r1)
	
r2 = RuleDescriptor()
r2.name = "dollar-stroke-wdth"
r2.conditions.append(dict(name="wdth", minimum=75, maximum=85))
r2.subs.append(("dollar", "dollar.rvrn"))
doc.addRule(r2)


doc.write(designSpace)

default = "RobotoExtremo-Regular.ufo"
# load the default font
default_path = os.path.join(src_dir, default)
dflt = Font(default_path)

sources = [source.name for source in doc.sources]
# take the default out of the source list
sources.remove(default)

print ("Building masters...")

# load font objects
fonts = []
accentFonts = []
for fileName in sources:
	source_path = os.path.join(src_dir, fileName)
	master_path = os.path.join(master_dir, fileName)
	if os.path.exists(master_path):
		# use this updated instance
		font = Font(master_path)
	else:
		font = Font(source_path)
	if fileName not in ['RobotoExtremo-opszmax.ufo', 'RobotoExtremo-wghtmin.ufo', 'RobotoExtremo-wghtmax.ufo', 'RobotoExtremo-wdthmax.ufo', 'RobotoExtremo-wdthmin.ufo']:
	    accentFonts.append(font)
	fonts.append(font)
	
buildGlyphSet(dflt, fonts)
allfonts = [dflt]+fonts
#buildComposites(composites, accentFonts)
setGlyphOrder(glyphOrder, allfonts)
clearAnchors(allfonts)
saveMasters(allfonts)

# build Variable Font

ufos = [font.path for font in allfonts]
project = FontProject()
project.run_from_ufos(
	ufos, 
	output=("ttf-interpolatable"), # FIXME this also build master_ttf and should not.
	remove_overlaps=False, 
	reverse_direction=False, 
	use_production_names=False)

#temp changed rel path to work in same dir, was:  ../fonts/RobotoExtremo-VF.ttf
outfile = "RobotoExtremo-VF.ttf"

#make folder if it doesn't exist
destFolder = "fonts"
if not os.path.exists(destFolder):
    os.makedirs(destFolder)
outfile = os.path.join(destFolder, outfile)



finder = lambda s: s.replace("master_ufo", "master_ttf").replace(".ufo", ".ttf")



varfont, _, _ = build(designSpace, finder)
print ("Saving Variable Font...")
varfont.save(outfile)

print ("Cleaning up...")

# clean up previous build
if os.path.exists("instances"):
	shutil.rmtree("instances", ignore_errors=True)
if os.path.exists("master_ttf"):
	shutil.rmtree("master_ttf", ignore_errors=True)
if os.path.exists("master_ufo"):
	shutil.rmtree("master_ufo", ignore_errors=True)
if os.path.exists("master_ttf_interpolatable"):
	shutil.rmtree("master_ttf_interpolatable", ignore_errors=True)


print ("DONE!")

# SUBSET COMMAND
# pyftsubset RobotoExtremo-VF.ttf --text-file=ascii-subset.txt --output-file=RobotoExtremo-subset-VF.ttf
