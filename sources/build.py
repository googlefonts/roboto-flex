# License: Apache 2.0

from glyphNameFormatter.data import name2unicode_AGD
from mutatorMath.ufo.document import DesignSpaceDocumentWriter, DesignSpaceDocumentReader
from designSpaceDocument import DesignSpaceDocument, SourceDescriptor, InstanceDescriptor, AxisDescriptor
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

def buildComposites(composites, fonts):
	# build the composites
	for font in fonts:
		for glyphName in composites.keys():
			font.newGlyph(glyphName)
			composite = font[glyphName]
			composite.unicode = name2unicode_AGD[glyphName]
			
			value = composites[glyphName]
			items = value.split("+")
			base = items[0]
			items = items[1:]
	
			component = composite.instantiateComponent()
			component.baseGlyph = base
			baseGlyph = font[base]
			composite.width = baseGlyph.width
			composite.appendComponent(component)
	
			for item in items:
				baseName, anchorName = item.split("@")
				component = composite.instantiateComponent()
				component.baseGlyph = baseName
				anchor = _anchor = None
				for a in baseGlyph.anchors:
					if a["name"] == anchorName:
						anchor = a
				for a in font[baseName].anchors:
					if a["name"] == "_"+anchorName:
						_anchor = a
				if anchor and _anchor:
					x = anchor["x"] - _anchor["x"]
					y = anchor["y"] - _anchor["y"]
					component.move((x, y))
				composite.appendComponent(component)
			composite.lib['com.typemytype.robofont.mark'] = [0, 0, 0, 0.5] # grey

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
		font.save(path)

with open("RobotoDelta.enc") as enc:
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

print "Cleaning up..."

# clean up previous build
if os.path.exists("instances"):
	shutil.rmtree("instances", ignore_errors=True)
if os.path.exists("master_ttf"):
	shutil.rmtree("master_ttf", ignore_errors=True)
if os.path.exists("master_ufo"):
	shutil.rmtree("master_ufo", ignore_errors=True)
if os.path.exists("master_ttf_interpolatable"):
	shutil.rmtree("master_ttf_interpolatable", ignore_errors=True)

src_dir = "1-drawings"
master_dir = "master_ufo"
instance_dir = "instances"

# use a temporary designspace to build instances with mutator math
familyName = "RobotoDelta"
tmpDesignSpace = "tmp.designspace"
doc = DesignSpaceDocumentWriter(tmpDesignSpace)
# sources
doc.addSource(path="1-drawings/RobotoDelta-Regular.ufo", name="RobotoDelta-Regular.ufo", location=dict(XYOPQ=0, XTRA=0, YTLC=0, YTUC=0, YTAS=0, YTDE=0), styleName="Regular", familyName=familyName, copyLib=False, copyGroups=False, copyInfo=False, copyFeatures=False, muteKerning=False, muteInfo=False, mutedGlyphNames=None)
doc.addSource(path="1-drawings/RobotoDelta-XOPQmin-YOPQmin.ufo", name="RobotoDelta-XOPQmin-YOPQmin.ufo", location=dict(XYOPQ=-1), styleName="XOPQmin-YOPQmin", familyName=familyName, copyLib=False, copyGroups=False, copyInfo=False, copyFeatures=False, muteKerning=False, muteInfo=False, mutedGlyphNames=None)
doc.addSource(path="1-drawings/RobotoDelta-XOPQmax-YOPQmax.ufo", name="RobotoDelta-XOPQmax-YOPQmax.ufo", location=dict(XYOPQ=1), styleName="XOPQmax-YOPQmax", familyName=familyName, copyLib=False, copyGroups=False, copyInfo=False, copyFeatures=False, muteKerning=False, muteInfo=False, mutedGlyphNames=None)
doc.addSource(path="1-drawings/RobotoDelta-XTRAmin.ufo", name="RobotoDelta-XTRAmin.ufo", location=dict(XTRA=-1), styleName="XTRAmin", familyName=familyName, copyLib=False, copyGroups=False, copyInfo=False, copyFeatures=False, muteKerning=False, muteInfo=False, mutedGlyphNames=None)
doc.addSource(path="1-drawings/RobotoDelta-XTRAmax.ufo", name="RobotoDelta-XTRAmax.ufo", location=dict(XTRA=1), styleName="XTRAmax", familyName=familyName, copyLib=False, copyGroups=False, copyInfo=False, copyFeatures=False, muteKerning=False, muteInfo=False, mutedGlyphNames=None)
doc.addSource(path="1-drawings/RobotoDelta-YTLCmin.ufo", name="RobotoDelta-YTLCmin.ufo", location=dict(YTLC=-1), styleName="YTLCmin", familyName=familyName, copyLib=False, copyGroups=False, copyInfo=False, copyFeatures=False, muteKerning=False, muteInfo=False, mutedGlyphNames=None)
doc.addSource(path="1-drawings/RobotoDelta-YTLCmax.ufo", name="RobotoDelta-YTLCmax.ufo", location=dict(YTLC=1), styleName="YTLCmax", familyName=familyName, copyLib=False, copyGroups=False, copyInfo=False, copyFeatures=False, muteKerning=False, muteInfo=False, mutedGlyphNames=None)
doc.addSource(path="1-drawings/RobotoDelta-YTUCmin.ufo", name="RobotoDelta-YTUCmin.ufo", location=dict(YTUC=-1), styleName="YTUCmin", familyName=familyName, copyLib=False, copyGroups=False, copyInfo=False, copyFeatures=False, muteKerning=False, muteInfo=False, mutedGlyphNames=None)
doc.addSource(path="1-drawings/RobotoDelta-YTUCmax.ufo", name="RobotoDelta-YTUCmax.ufo", location=dict(YTUC=1), styleName="YTUCmax", familyName=familyName, copyLib=False, copyGroups=False, copyInfo=False, copyFeatures=False, muteKerning=False, muteInfo=False, mutedGlyphNames=None)
doc.addSource(path="1-drawings/RobotoDelta-YTASmin.ufo", name="RobotoDelta-YTASmin.ufo", location=dict(YTAS=-1), styleName="YTASmin", familyName=familyName, copyLib=False, copyGroups=False, copyInfo=False, copyFeatures=False, muteKerning=False, muteInfo=False, mutedGlyphNames=None)
doc.addSource(path="1-drawings/RobotoDelta-YTASmax.ufo", name="RobotoDelta-YTASmax.ufo", location=dict(YTAS=1), styleName="YTASmax", familyName=familyName, copyLib=False, copyGroups=False, copyInfo=False, copyFeatures=False, muteKerning=False, muteInfo=False, mutedGlyphNames=None)
doc.addSource(path="1-drawings/RobotoDelta-YTDEmin.ufo", name="RobotoDelta-YTDEmin.ufo", location=dict(YTDE=-1), styleName="YTDEmin", familyName=familyName, copyLib=False, copyGroups=False, copyInfo=False, copyFeatures=False, muteKerning=False, muteInfo=False, mutedGlyphNames=None)
doc.addSource(path="1-drawings/RobotoDelta-YTDEmax.ufo", name="RobotoDelta-YTDEmax.ufo", location=dict(YTDE=1), styleName="YTDEmax", familyName=familyName, copyLib=False, copyGroups=False, copyInfo=False, copyFeatures=False, muteKerning=False, muteInfo=False, mutedGlyphNames=None)
# axes
doc.addAxis(tag="XYOPQ", name="XYOPQ", minimum=-1, maximum=1, default=0, warpMap=None)
doc.addAxis(tag="XTRA", name="XTRA", minimum=-1, maximum=1, default=0, warpMap=None)
doc.addAxis(tag="YTLC", name="YTLC", minimum=-1, maximum=1, default=0, warpMap=None)
doc.addAxis(tag="YTUC", name="YTUC", minimum=-1, maximum=1, default=0, warpMap=None)
doc.addAxis(tag="YTAS", name="YTAS", minimum=-1, maximum=1, default=0, warpMap=None)
doc.addAxis(tag="YTDE", name="YTDE", minimum=-1, maximum=1, default=0, warpMap=None)
# instances
instances = [
	dict(fileName="instances/RobotoDelta-XOPQmin.ufo", location=dict(XYOPQ=(-1, 0)), styleName="XOPQmin", familyName=familyName, postScriptFontName=None, styleMapFamilyName=None, styleMapStyleName=None),
	dict(fileName="instances/RobotoDelta-XOPQmax.ufo", location=dict(XYOPQ=(1, 0)), styleName="XOPQmax", familyName=familyName, postScriptFontName=None, styleMapFamilyName=None, styleMapStyleName=None),
	dict(fileName="instances/RobotoDelta-YOPQmin.ufo", location=dict(XYOPQ=(0, -1)), styleName="YOPQmin", familyName=familyName, postScriptFontName=None, styleMapFamilyName=None, styleMapStyleName=None),
	dict(fileName="instances/RobotoDelta-YOPQmax.ufo", location=dict(XYOPQ=(0, 1)), styleName="YOPQmax", familyName=familyName, postScriptFontName=None, styleMapFamilyName=None, styleMapStyleName=None),
	dict(fileName="instances/RobotoDelta-XOPQmin-YOPQmin-XTRAmin.ufo", location=dict(XYOPQ=-1, XTRA=-1), styleName="XOPQmin-YOPQmin-XTRAmin", familyName=familyName, postScriptFontName=None, styleMapFamilyName=None, styleMapStyleName=None),
	dict(fileName="instances/RobotoDelta-XOPQmin-YOPQmin-XTRAmax.ufo", location=dict(XYOPQ=-1, XTRA=1), styleName="XOPQmin-YOPQmin-XTRAmax", familyName=familyName, postScriptFontName=None, styleMapFamilyName=None, styleMapStyleName=None),
	
	dict(fileName="instances/RobotoDelta-YTRAmin.ufo", location=dict(YTLC=-1, YTUC=-1, YTAS=-1, YTDE=1), styleName="YTRAmin", familyName=familyName, postScriptFontName=None, styleMapFamilyName=None, styleMapStyleName=None),
	dict(fileName="instances/RobotoDelta-YTRAmax.ufo", location=dict(YTLC=1, YTUC=1, YTAS=1, YTDE=-1), styleName="YTRAmax", familyName=familyName, postScriptFontName=None, styleMapFamilyName=None, styleMapStyleName=None),
		
	dict(fileName="instances/RobotoDelta-opszmin.ufo", location=dict(XYOPQ=(0.08, 0.12), XTRA=0.16, YTLC=0.32), styleName="opszmin", familyName=familyName, postScriptFontName=None, styleMapFamilyName=None, styleMapStyleName=None),
	dict(fileName="instances/RobotoDelta-opsz36.ufo", location=dict(XYOPQ=(-0.24, -0.18), XTRA=-0.18, YTLC=-0.265), styleName="opsz36", familyName=familyName, postScriptFontName=None, styleMapFamilyName=None, styleMapStyleName=None),
	dict(fileName="instances/RobotoDelta-wghtmin.ufo", location=dict(XYOPQ=(-0.74, -0.68), XTRA=0.16), styleName="wghtmin", familyName=familyName, postScriptFontName=None, styleMapFamilyName=None, styleMapStyleName=None),
#	dict(fileName="instances/RobotoDelta-wghtmax.ufo", location=dict(XYOPQ=(0.74, 0.5), XTRA=-0.5, YTLC=0.23), styleName="wghtmax", familyName=familyName, postScriptFontName=None, styleMapFamilyName=None, styleMapStyleName=None),

#	dict(fileName="instances/RobotoDelta-wdthmin.ufo", location=dict(XYOPQ=(-0.12, -0.09), XTRA=-1.00), styleName="wdthmin", familyName=familyName, postScriptFontName=None, styleMapFamilyName=None, styleMapStyleName=None),
#	dict(fileName="instances/RobotoDelta-wdthmax.ufo", location=dict(XYOPQ=(0.12, 0.09), XTRA=1.00), styleName="wdthmax", familyName=familyName, postScriptFontName=None, styleMapFamilyName=None, styleMapStyleName=None),
]
for instance in instances:
	doc.startInstance(**instance)
	doc.writeInfo()
	doc.writeKerning()
	doc.endInstance()

doc.save()
# read and process the designspace
doc = DesignSpaceDocumentReader(tmpDesignSpace, ufoVersion=2, roundGeometry=False, verbose=False)
print "Reading DesignSpace..."
doc.process(makeGlyphs=True, makeKerning=True, makeInfo=True)
os.remove(tmpDesignSpace) # clean up

# update the instances with the source fonts
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

designSpace = "RobotoDelta.designspace"
sources = [
	dict(path="master_ufo/RobotoDelta-Regular.ufo", name="RobotoDelta-Regular.ufo", location=dict(XOPQ=94, YOPQ=77, XTRA=359, YTLC=514, YTUC=712, YTAS=750, YTDE=-203, YTAD=563, YTDD=0, UDLN=-49, wght=400, wdth=100, opsz=12, PWGT=94, PWDT=712, POPS=0, GRAD=0, YTRA=0), styleName="Regular", familyName=familyName, copyInfo=True),	
	dict(path="master_ufo/RobotoDelta-XOPQmin.ufo", name="RobotoDelta-XOPQmin.ufo", location=dict(XOPQ=26), styleName="XOPQmin", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoDelta-XOPQmax.ufo", name="RobotoDelta-XOPQmax.ufo", location=dict(XOPQ=171), styleName="XOPQmax", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoDelta-YOPQmin.ufo", name="RobotoDelta-YOPQmin.ufo", location=dict(YOPQ=26), styleName="YOPQmin", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoDelta-YOPQmax.ufo", name="RobotoDelta-YOPQmax.ufo", location=dict(YOPQ=132), styleName="YOPQmax", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoDelta-XOPQmin-YOPQmin.ufo", name="RobotoDelta-XOPQmin-YOPQmin.ufo", location=dict(XOPQ=26, YOPQ=26), styleName="XOPQmin-YOPQmin", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoDelta-XOPQmax-YOPQmax.ufo", name="RobotoDelta-XOPQmax-YOPQmax.ufo", location=dict(XOPQ=171, YOPQ=132), styleName="XOPQmax-YOPQmax", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoDelta-XTRAmin.ufo", name="RobotoDelta-XTRAmin.ufo", location=dict(XTRA=210), styleName="XTRAmin", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoDelta-XTRAmax.ufo", name="RobotoDelta-XTRAmax.ufo", location=dict(XTRA=513), styleName="XTRAmax", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoDelta-XOPQmin-YOPQmin-XTRAmin.ufo", name="RobotoDelta-XOPQmin-YOPQmin-XTRAmin.ufo", location=dict(XOPQ=26, YOPQ=26, XTRA=210), styleName="XOPQmin-YOPQmin-XTRAmin", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoDelta-XOPQmin-YOPQmin-XTRAmax.ufo", name="RobotoDelta-XOPQmin-YOPQmin-XTRAmax.ufo", location=dict(XOPQ=26, YOPQ=26, XTRA=513), styleName="XOPQmin-YOPQmin-XTRAmin", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoDelta-YTLCmin.ufo", name="RobotoDelta-YTLCmin.ufo", location=dict(YTLC=416), styleName="YTLCmin", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoDelta-YTLCmax.ufo", name="RobotoDelta-YTLCmax.ufo", location=dict(YTLC=570), styleName="YTLCmax", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoDelta-YTUCmin.ufo", name="RobotoDelta-YTUCmin.ufo", location=dict(YTUC=528), styleName="YTUCmin", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoDelta-YTUCmax.ufo", name="RobotoDelta-YTUCmax.ufo", location=dict(YTUC=760), styleName="YTUCmax", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoDelta-YTASmin.ufo", name="RobotoDelta-YTASmin.ufo", location=dict(YTAS=649), styleName="YTASmin", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoDelta-YTASmax.ufo", name="RobotoDelta-YTASmax.ufo", location=dict(YTAS=854), styleName="YTASmax", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoDelta-YTDEmin.ufo", name="RobotoDelta-YTDEmin.ufo", location=dict(YTDE=-305), styleName="YTDEmin", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoDelta-YTDEmax.ufo", name="RobotoDelta-YTDEmax.ufo", location=dict(YTDE=-98), styleName="YTDEmax", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoDelta-YTADmin.ufo", name="RobotoDelta-YTADmin.ufo", location=dict(YTAD=460), styleName="YTADmin", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoDelta-YTADmax.ufo", name="RobotoDelta-YTADmax.ufo", location=dict(YTAD=600), styleName="YTADmax", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoDelta-YTDDmin.ufo", name="RobotoDelta-YTDDmin.ufo", location=dict(YTDD=-1), styleName="YTDDmin", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoDelta-YTDDmax.ufo", name="RobotoDelta-YTDDmax.ufo", location=dict(YTDD=1), styleName="YTDDmax", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoDelta-UDLNmin.ufo", name="RobotoDelta-UDLNmin.ufo", location=dict(UDLN=-195), styleName="UDLNmin", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoDelta-UDLNmax.ufo", name="RobotoDelta-UDLNmax.ufo", location=dict(UDLN=0), styleName="UDLNmax", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoDelta-YTRAmin.ufo", name="RobotoDelta-YTRAmin.ufo", location=dict(YTRA=-1), styleName="YTRAmin", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoDelta-YTRAmax.ufo", name="RobotoDelta-YTRAmax.ufo", location=dict(YTRA=1), styleName="YTRAmax", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoDelta-GRADmin.ufo", name="RobotoDelta-GRADmin.ufo", location=dict(GRAD=-1), styleName="GRADmin", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoDelta-GRADmax.ufo", name="RobotoDelta-GRADmax.ufo", location=dict(GRAD=1), styleName="GRADmax", familyName=familyName, copyInfo=False),
		
	dict(path="master_ufo/RobotoDelta-wghtmin.ufo", name="RobotoDelta-wghtmin.ufo", location=dict(wght=100), styleName="wghtmin", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoDelta-wghtmax.ufo", name="RobotoDelta-wghtmax.ufo", location=dict(wght=900), styleName="wghtmax", familyName=familyName, copyInfo=False),


	dict(path="master_ufo/RobotoDelta-wghtmin.ufo", name="RobotoDelta-wghtmin.ufo", location=dict(PWGT=44), styleName="wghtmin", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoDelta-wghtmax.ufo", name="RobotoDelta-wghtmax.ufo", location=dict(PWGT=150), styleName="wghtmax", familyName=familyName, copyInfo=False),
	
	dict(path="master_ufo/RobotoDelta-opszmin.ufo", name="RobotoDelta-opszmin.ufo", location=dict(opsz=8), styleName="opszmin", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoDelta-opsz36.ufo", name="RobotoDelta-opsz36.ufo", location=dict(opsz=36), styleName="opsz36", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoDelta-opszmax.ufo", name="RobotoDelta-opszmax.ufo", location=dict(opsz=144), styleName="opszmax", familyName=familyName, copyInfo=False),

	dict(path="master_ufo/RobotoDelta-wdthmin.ufo", name="RobotoDelta-wdthmin.ufo", location=dict(wdth=75), styleName="wdthmin", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoDelta-wdthmax.ufo", name="RobotoDelta-wdthmax.ufo", location=dict(wdth=125), styleName="wdthmax", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoDelta-wdthmin.ufo", name="RobotoDelta-wdthmin.ufo", location=dict(PWDT=560), styleName="wdthmin", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoDelta-wdthmax.ufo", name="RobotoDelta-wdthmax.ufo", location=dict(PWDT=867), styleName="wdthmax", familyName=familyName, copyInfo=False),
	
	
	dict(path="master_ufo/RobotoDelta-opszmax-wdthmax.ufo", name="RobotoDelta-opszmax-wdthmax.ufo", location=dict(wdth=125, opsz=144), styleName="opszmax-wdthmax", familyName=familyName, copyInfo=False),

	dict(path="master_ufo/RobotoDelta-opszmax-wdthmin.ufo", name="RobotoDelta-opszmax-wdthmin.ufo", location=dict(wdth=75, opsz=144), styleName="opszmax-wdthmin", familyName=familyName, copyInfo=False),
	
	dict(path="master_ufo/RobotoDelta-wghtmax-opszmax.ufo", name="RobotoDelta-wghtmax-opszmax.ufo", location=dict(wght=900, opsz=144), styleName="wghtmax-opszmax", familyName=familyName, copyInfo=False),
	
		dict(path="master_ufo/RobotoDelta-wghtmin-opszmax.ufo", name="RobotoDelta-wghtmin-opszmax.ufo", location=dict(wght=100, opsz=144), styleName="wghtmin-opszmax", familyName=familyName, copyInfo=False),

		
	dict(path="master_ufo/RobotoDelta-opszmax-wghtmax-wdthmax.ufo", name="RobotoDelta-opszmax-wghtmax-wdthmax.ufo", location=dict(wght=900, opsz=144, wdth=125), styleName="opszmax-wghtmax-wdthmax", familyName=familyName, copyInfo=False),
	
	dict(path="master_ufo/RobotoDelta-opszmax-wghtmax-wdthmin.ufo", name="RobotoDelta-opszmax-wghtmax-wdthmin.ufo", location=dict(wght=900, opsz=144, wdth=75), styleName="opszmax-wghtmax-wdthmin", familyName=familyName, copyInfo=False),
		
	
	
	
]
instances = []
axes = [
	dict(minimum=210, maximum=513, default=359, name="XTRA", tag="XTRA", labelNames={"en": "XTRA"}, map=[]),
	dict(minimum=26, maximum=171, default=94, name="XOPQ", tag="XOPQ", labelNames={"en": "XOPQ"}, map=[]),
	dict(minimum=26, maximum=132, default=77, name="YOPQ", tag="YOPQ", labelNames={"en": "YOPQ"}, map=[]),
	dict(minimum=416, maximum=570, default=514, name="YTLC", tag="YTLC", labelNames={"en": "YTLC"}, map=[]),
	dict(minimum=528, maximum=760, default=712, name="YTUC", tag="YTUC", labelNames={"en": "YTUC"}, map=[]),
	dict(minimum=649, maximum=854, default=750, name="YTAS", tag="YTAS", labelNames={"en": "YTAS"}, map=[]),
	dict(minimum=-305, maximum=-98, default=-203, name="YTDE", tag="YTDE", labelNames={"en": "YTDE"}, map=[]),
	dict(minimum=460, maximum=600, default=563, name="YTAD", tag="YTAD", labelNames={"en": "YTAD"}, map=[]),
	dict(minimum=-1, maximum=1, default=0, name="YTDD", tag="YTDD", labelNames={"en": "YTDD"}, map=[]),
	dict(minimum=-195, maximum=0, default=-49, name="UDLN", tag="UDLN", labelNames={"en": "UDLN"}, map=[]),
	dict(minimum=100, maximum=900, default=400, name="wght", tag="wght", labelNames={"en": "wght"}, map=[]),
	dict(minimum=75, maximum=125, default=100, name="wdth", tag="wdth", labelNames={"en": "wdth"}, map=[]),
	dict(minimum=8, maximum=144, default=12, name="opsz", tag="opsz", labelNames={"en": "opsz"}, map=[]),
	dict(minimum=44, maximum=150, default=94, name="PWGT", tag="PWGT", labelNames={"en": "PWGT"}, map=[]),
	dict(minimum=560, maximum=867, default=712, name="PWDT", tag="PWDT", labelNames={"en": "PWDT"}, map=[]),
	dict(minimum=-1, maximum=1, default=0, name="POPS", tag="POPS", labelNames={"en": "POPS"}, map=[]),
	dict(minimum=-1, maximum=1, default=0, name="GRAD", tag="GRAD", labelNames={"en": "GRAD"}, map=[]),
	dict(minimum=-1, maximum=1, default=0, name="YTRA", tag="YTRA", labelNames={"en": "YTRA"}, map=[]),
]

doc = buildDesignSpace(sources, instances, axes)
doc.write(designSpace)

default = "RobotoDelta-Regular.ufo"
# load the default font
default_path = os.path.join(src_dir, default)
dflt = Font(default_path)

sources = [source.name for source in doc.sources]
# take the default out of the source list
sources.remove(default)

print "Building masters..."

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
	if fileName not in ['RobotoDelta-opszmax.ufo', 'RobotoDelta-wghtmin.ufo', 'RobotoDelta-wghtmax.ufo', 'RobotoDelta-wdthmax.ufo', 'RobotoDelta-wdthmin.ufo']:
	    accentFonts.append(font)
	fonts.append(font)
	
buildGlyphSet(dflt, fonts)
allfonts = [dflt]+fonts
buildComposites(composites, accentFonts)
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

outfile = "../fonts/RobotoDelta-VF.ttf"
finder = lambda s: s.replace("master_ufo", "master_ttf_interpolatable").replace(".ufo", ".ttf")
varfont, _, _ = build(designSpace, finder)
print "Saving Variable Font..."
varfont.save(outfile)

print "DONE!"
