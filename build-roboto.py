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
from distutils.dir_util import copy_tree
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

# Remove temporary 1-drawings
if os.path.exists("sources/1-drawings"):
	shutil.rmtree("sources/1-drawings", ignore_errors=True)


# New
src = {	"sources/1A-drawings/Mains",
		"sources/1A-drawings/Parametric Axes",
		"sources/1A-drawings/Duovars",
		"sources/1A-drawings/Trivars",
		"sources/1A-drawings/Quadravars",
		
		}
	

src_dir = "sources/1-drawings"
master_dir = "master_ufo"
instance_dir = "instances"

# Copy sources to temporary 1-drawings
for source in src:
	copy_tree(source, src_dir)


# use a temporary designspace to build instances with mutator math
familyName = "RobotoExtremo"
tmpDesignSpace = "tmp.designspace"
doc = DesignSpaceDocumentWriter(tmpDesignSpace)
# sources
doc.addSource(path="sources/1-drawings/RobotoExtremo-Regular.ufo", name="RobotoExtremo-Regular.ufo", location=dict(wght=0, wdth=0, opsz=0), styleName="Regular", familyName=familyName, copyLib=False, copyGroups=False, copyInfo=False, copyFeatures=False, muteKerning=False, muteInfo=False, mutedGlyphNames=None)
# doc.addSource(path="sources/1-drawings/RobotoExtremo-XOPQ27-YOPQ25.ufo", name="RobotoExtremo-XOPQ27-YOPQ25.ufo", location=dict(XYOPQ=-1), styleName="XOPQ27-YOPQ25", familyName=familyName, copyLib=False, copyGroups=False, copyInfo=False, copyFeatures=False, muteKerning=False, muteInfo=False, mutedGlyphNames=None)
# doc.addSource(path="sources/1-drawings/RobotoExtremo-XOPQ175-YOPQ135.ufo", name="RobotoExtremo-XOPQ175-YOPQ135.ufo", location=dict(XYOPQ=1), styleName="XOPQ175-YOPQ135", familyName=familyName, copyLib=False, copyGroups=False, copyInfo=False, copyFeatures=False, muteKerning=False, muteInfo=False, mutedGlyphNames=None)
# doc.addSource(path="sources/1-drawings/RobotoExtremo-XTRA323.ufo", name="RobotoExtremo-XTRA323.ufo", location=dict(XTRA=-1), styleName="XTRA323", familyName=familyName, copyLib=False, copyGroups=False, copyInfo=False, copyFeatures=False, muteKerning=False, muteInfo=False, mutedGlyphNames=None)
# doc.addSource(path="sources/1-drawings/RobotoExtremo-XTRA603.ufo", name="RobotoExtremo-XTRA603.ufo", location=dict(XTRA=1), styleName="XTRA603", familyName=familyName, copyLib=False, copyGroups=False, copyInfo=False, copyFeatures=False, muteKerning=False, muteInfo=False, mutedGlyphNames=None)
# doc.addSource(path="sources/1-drawings/RobotoExtremo-YTLC416.ufo", name="RobotoExtremo-YTLC416.ufo", location=dict(YTLC=-1), styleName="YTLC416", familyName=familyName, copyLib=False, copyGroups=False, copyInfo=False, copyFeatures=False, muteKerning=False, muteInfo=False, mutedGlyphNames=None)
# doc.addSource(path="sources/1-drawings/RobotoExtremo-YTLC570.ufo", name="RobotoExtremo-YTLC570.ufo", location=dict(YTLC=1), styleName="YTLC570", familyName=familyName, copyLib=False, copyGroups=False, copyInfo=False, copyFeatures=False, muteKerning=False, muteInfo=False, mutedGlyphNames=None)
# doc.addSource(path="sources/1-drawings/RobotoExtremo-YTUC528.ufo", name="RobotoExtremo-YTUC528.ufo", location=dict(YTUC=-1), styleName="YTUC528", familyName=familyName, copyLib=False, copyGroups=False, copyInfo=False, copyFeatures=False, muteKerning=False, muteInfo=False, mutedGlyphNames=None)
# doc.addSource(path="sources/1-drawings/RobotoExtremo-YTUC760.ufo", name="RobotoExtremo-YTUC760.ufo", location=dict(YTUC=1), styleName="YTUC760", familyName=familyName, copyLib=False, copyGroups=False, copyInfo=False, copyFeatures=False, muteKerning=False, muteInfo=False, mutedGlyphNames=None)
# doc.addSource(path="sources/1-drawings/RobotoExtremo-YTAS649.ufo", name="RobotoExtremo-YTAS649.ufo", location=dict(YTAS=-1), styleName="YTAS649", familyName=familyName, copyLib=False, copyGroups=False, copyInfo=False, copyFeatures=False, muteKerning=False, muteInfo=False, mutedGlyphNames=None)
# doc.addSource(path="sources/1-drawings/RobotoExtremo-YTAS854.ufo", name="RobotoExtremo-YTAS854.ufo", location=dict(YTAS=1), styleName="YTAS854", familyName=familyName, copyLib=False, copyGroups=False, copyInfo=False, copyFeatures=False, muteKerning=False, muteInfo=False, mutedGlyphNames=None)
# doc.addSource(path="sources/1-drawings/RobotoExtremo-YTDE-305.ufo", name="RobotoExtremo-YTDE-305.ufo", location=dict(YTDE=-1), styleName="YTDE-305", familyName=familyName, copyLib=False, copyGroups=False, copyInfo=False, copyFeatures=False, muteKerning=False, muteInfo=False, mutedGlyphNames=None)
# doc.addSource(path="sources/1-drawings/RobotoExtremo-YTDE-98.ufo", name="RobotoExtremo-YTDE-98.ufo", location=dict(YTDE=1), styleName="YTDE-98", familyName=familyName, copyLib=False, copyGroups=False, copyInfo=False, copyFeatures=False, muteKerning=False, muteInfo=False, mutedGlyphNames=None)

# axes
doc.addAxis(tag="wght", name="wght", minimum=100, maximum=900, default=400, warpMap=None)
doc.addAxis(tag="wdth", name="wdth", minimum=75, maximum=125, default=100, warpMap=None)
doc.addAxis(tag="opsz", name="opsz", minimum=8, maximum=144, default=14, warpMap=None)






# instances
instances = [
#	dict(fileName="instances/RobotoExtremo-opsz144-wght100-wdth151.ufo", location=dict(wght=100, wdth=125, opsz=144), styleName="opsz144-wght100-wdth151", familyName=familyName, postScriptFontName=None, styleMapFamilyName=None, styleMapStyleName=None),
#	dict(fileName="instances/RobotoExtremo-opsz144-wght100-wdth075.ufo", location=dict(wght=100, wdth=87, opsz=144), styleName="opsz144-wght100-wdth075", familyName=familyName, postScriptFontName=None, styleMapFamilyName=None, styleMapStyleName=None),
#	dict(fileName="instances/RobotoExtremo-opsz144-wght100-wdth25.ufo", location=dict(wght=100, wdth=75, opsz=144), styleName="opsz144-wght100-wdth25", familyName=familyName, postScriptFontName=None, styleMapFamilyName=None, styleMapStyleName=None),
	
#	dict(fileName="instances/RobotoExtremo-opsz144-wght900-wdth151.ufo", location=dict(wght=900, wdth=125, opsz=144), styleName="opsz144-wght900-wdth151", familyName=familyName, postScriptFontName=None, styleMapFamilyName=None, styleMapStyleName=None),
#	dict(fileName="instances/RobotoExtremo-opsz144-wght900-wdth075.ufo", location=dict(wght=900, wdth=76, opsz=144), styleName="opsz144-wght900-wdth075", familyName=familyName, postScriptFontName=None, styleMapFamilyName=None, styleMapStyleName=None),
#	dict(fileName="instances/RobotoExtremo-opsz144-wght900-wdth25.ufo", location=dict(wght=900, wdth=75, opsz=144), styleName="opsz144-wght900-wdth25", familyName=familyName, postScriptFontName=None, styleMapFamilyName=None, styleMapStyleName=None),
	
#	dict(fileName="instances/RobotoExtremo-opsz144-wdth151.ufo", location=dict(wght=400, wdth=125, opsz=144), styleName="opsz144-wdth151", familyName=familyName, postScriptFontName=None, styleMapFamilyName=None, styleMapStyleName=None),
#	dict(fileName="instances/RobotoExtremo-opsz144-wdth075.ufo", location=dict(wght=400, wdth=80, opsz=144), styleName="opsz144-wdth075", familyName=familyName, postScriptFontName=None, styleMapFamilyName=None, styleMapStyleName=None),
#	dict(fileName="instances/RobotoExtremo-opsz144-wdth25.ufo", location=dict(wght=400, wdth=75, opsz=144), styleName="opsz144-wdth25", familyName=familyName, postScriptFontName=None, styleMapFamilyName=None, styleMapStyleName=None),
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
	
##	Main 
	dict(path="master_ufo/RobotoExtremo-GRAD-1.ufo", name="RobotoExtremo-GRAD-1.ufo", location=dict(GRAD=-1), styleName="GRAD-1", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-GRAD1.ufo", name="RobotoExtremo-GRAD1.ufo", location=dict(GRAD=1), styleName="GRAD1", familyName=familyName, copyInfo=False),
		
	dict(path="master_ufo/RobotoExtremo-wght100.ufo", name="RobotoExtremo-wght100.ufo", location=dict(wght=100), styleName="wght100", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-wght900.ufo", name="RobotoExtremo-wght900.ufo", location=dict(wght=900), styleName="wght900", familyName=familyName, copyInfo=False),


# 	dict(path="master_ufo/RobotoExtremo-wght100.ufo", name="RobotoExtremo-wght100.ufo", location=dict(PWGT=44), styleName="wght100", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-wght900.ufo", name="RobotoExtremo-wght900.ufo", location=dict(PWGT=150), styleName="wght900", familyName=familyName, copyInfo=False),
	
	dict(path="master_ufo/RobotoExtremo-opsz8.ufo", name="RobotoExtremo-opsz8.ufo", location=dict(opsz=8), styleName="opsz8", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-opsz36.ufo", name="RobotoExtremo-opsz36.ufo", location=dict(opsz=36), styleName="opsz36", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz144.ufo", name="RobotoExtremo-opsz144.ufo", location=dict(opsz=144), styleName="opsz144", familyName=familyName, copyInfo=False),

	dict(path="master_ufo/RobotoExtremo-wdth25.ufo", name="RobotoExtremo-wdth25.ufo", location=dict(wdth=25), styleName="wdth25", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-wdth151.ufo", name="RobotoExtremo-wdth151.ufo", location=dict(wdth=151), styleName="wdth151", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-wdth25.ufo", name="RobotoExtremo-wdth25.ufo", location=dict(PWDT=560), styleName="wdth25", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-wdth151.ufo", name="RobotoExtremo-wdth151.ufo", location=dict(PWDT=867), styleName="wdth151", familyName=familyName, copyInfo=False),

##	Parametric
	dict(path="master_ufo/RobotoExtremo-XOPQ27.ufo", name="RobotoExtremo-XOPQ27.ufo", location=dict(XOPQ=27), styleName="XOPQ27", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-XOPQ175.ufo", name="RobotoExtremo-XOPQ175.ufo", location=dict(XOPQ=175), styleName="XOPQ175", familyName=familyName, copyInfo=False),
	
	dict(path="master_ufo/RobotoExtremo-XTRA323.ufo", name="RobotoExtremo-XTRA323.ufo", location=dict(XTRA=323), styleName="XTRA323", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-XTRA603.ufo", name="RobotoExtremo-XTRA603.ufo", location=dict(XTRA=603), styleName="XTRA603", familyName=familyName, copyInfo=False),

	dict(path="master_ufo/RobotoExtremo-YOPQ25.ufo", name="RobotoExtremo-YOPQ25.ufo", location=dict(YOPQ=25), styleName="YOPQ25", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-YOPQ135.ufo", name="RobotoExtremo-YOPQ135.ufo", location=dict(YOPQ=135), styleName="YOPQ135", familyName=familyName, copyInfo=False),
	
# 	dict(path="master_ufo/RobotoExtremo-YOLCmin.ufo", name="RobotoExtremo-YOLCmin.ufo", location=dict(YOLC=25), styleName="YOLCmin", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-YOLCmax.ufo", name="RobotoExtremo-YOLCmax.ufo", location=dict(YOLC=130), styleName="YOLCmax", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-YOUCmin.ufo", name="RobotoExtremo-YOUCmin.ufo", location=dict(YOUC=25), styleName="YOUCmin", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-YOUCmax.ufo", name="RobotoExtremo-YOUCmax.ufo", location=dict(YOUC=135), styleName="YOUCmax", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-YOFImin.ufo", name="RobotoExtremo-YOFImin.ufo", location=dict(YOFI=25), styleName="YOFImin", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-YOFImax.ufo", name="RobotoExtremo-YOFImax.ufo", location=dict(YOFI=150), styleName="YOFImax", familyName=familyName, copyInfo=False),
 	
	dict(path="master_ufo/RobotoExtremo-YTLC416.ufo", name="RobotoExtremo-YTLC416.ufo", location=dict(YTLC=416), styleName="YTLC416", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-YTLC570.ufo", name="RobotoExtremo-YTLC570.ufo", location=dict(YTLC=570), styleName="YTLC570", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-YTUC528.ufo", name="RobotoExtremo-YTUC528.ufo", location=dict(YTUC=528), styleName="YTUC528", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-YTUC760.ufo", name="RobotoExtremo-YTUC760.ufo", location=dict(YTUC=760), styleName="YTUC760", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-YTAS649.ufo", name="RobotoExtremo-YTAS649.ufo", location=dict(YTAS=649), styleName="YTAS649", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-YTAS854.ufo", name="RobotoExtremo-YTAS854.ufo", location=dict(YTAS=854), styleName="YTAS854", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-YTDE-305.ufo", name="RobotoExtremo-YTDE-305.ufo", location=dict(YTDE=-305), styleName="YTDE-305", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-YTDE-98.ufo", name="RobotoExtremo-YTDE-98.ufo", location=dict(YTDE=-98), styleName="YTDE-98", familyName=familyName, copyInfo=False),

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

	
##	Duovars
	dict(path="master_ufo/RobotoExtremo-opsz144-wdth151.ufo", name="RobotoExtremo-opsz144-wdth151.ufo", location=dict(wdth=151, opsz=144), styleName="opsz144-wdth151", familyName=familyName, copyInfo=False),
#	dict(path="master_ufo/RobotoExtremo-opsz144-wdth075.ufo", name="RobotoExtremo-opsz144-wdth075.ufo", location=dict(wdth=80, opsz=144), styleName="opsz144-wdth25075", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz144-wdth25.ufo", name="RobotoExtremo-opsz144-wdth25.ufo", location=dict(wdth=25, opsz=144), styleName="opsz144-wdth25", familyName=familyName, copyInfo=False),
	
	dict(path="master_ufo/RobotoExtremo-opsz144-wght900.ufo", name="RobotoExtremo-opsz144-wght900.ufo", location=dict(wght=900, opsz=144), styleName="opsz144-wght900", familyName=familyName, copyInfo=False),
#	dict(path="master_ufo/RobotoExtremo-opsz144-wght780.ufo", name="RobotoExtremo-opsz144-wght780.ufo", location=dict(wght=780, opsz=144), styleName="opsz144-wght780", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz144-wght100.ufo", name="RobotoExtremo-opsz144-wght100.ufo", location=dict(wght=100, opsz=144), styleName="opsz144-wght100", familyName=familyName, copyInfo=False),
	
	dict(path="master_ufo/RobotoExtremo-opsz8-wdth151.ufo", name="RobotoExtremo-opsz8-wdth151.ufo", location=dict(wdth=151, opsz=8), styleName="opsz8-wdth151", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz8-wdth25.ufo", name="RobotoExtremo-opsz8-wdth25.ufo", location=dict(wdth=25, opsz=8), styleName="opsz8-wdth25", familyName=familyName, copyInfo=False),
	
	dict(path="master_ufo/RobotoExtremo-opsz8-wght900.ufo", name="RobotoExtremo-opsz8-wght900.ufo", location=dict(wght=900, opsz=8), styleName="opsz8-wght900", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz8-wght100.ufo", name="RobotoExtremo-opsz8-wght100.ufo", location=dict(wght=100, opsz=8), styleName="opsz8-wght100", familyName=familyName, copyInfo=False),
	
	
##	Trivars
	dict(path="master_ufo/RobotoExtremo-opsz144-wght100-wdth151.ufo", name="RobotoExtremo-opsz144-wght100-wdth151.ufo", location=dict(wght=100, wdth=151, opsz=144), styleName="opsz144-wght100-wdth151", familyName=familyName, copyInfo=False),
#	dict(path="master_ufo/RobotoExtremo-opsz144-wght100-wdth075.ufo", name="RobotoExtremo-opsz144-wght100-wdth075.ufo", location=dict(wght=100, wdth=87, opsz=144), styleName="opsz144-wght100-wdth075", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz144-wght100-wdth25.ufo", name="RobotoExtremo-opsz144-wght100-wdth25.ufo", location=dict(wght=100, wdth=25, opsz=144), styleName="opsz144-wght100-wdth25", familyName=familyName, copyInfo=False),
	
 	dict(path="master_ufo/RobotoExtremo-opsz144-wght900-wdth151.ufo", name="RobotoExtremo-opsz144-wght900-wdth151.ufo", location=dict(wght=900, opsz=144, wdth=151), styleName="opsz144-wght900-wdth151", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-opsz144-wght900-wdth075.ufo", name="RobotoExtremo-opsz144-wght900-wdth075.ufo", location=dict(wght=900, opsz=144, wdth=76), styleName="opsz144-wght900-wdth075", familyName=familyName, copyInfo=False),
 	dict(path="master_ufo/RobotoExtremo-opsz144-wght900-wdth25.ufo", name="RobotoExtremo-opsz144-wght900-wdth25.ufo", location=dict(wght=900, opsz=144, wdth=25), styleName="opsz144-wght900-wdth25", familyName=familyName, copyInfo=False),

	
	dict(path="master_ufo/RobotoExtremo-opsz8-wght900-wdth25.ufo", name="RobotoExtremo-opsz8-wght900-wdth25.ufo", location=dict(wdth=25, wght=900, opsz=8), styleName="opsz8-wght900-wdth25", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-wght900-wdth25.ufo", name="RobotoExtremo-wght900-wdth25.ufo", location=dict(wdth=25, wght=900), styleName="wght900-wdth25", familyName=familyName, copyInfo=False),


## Leveling intermediates
# 	dict(path="master_ufo/RobotoExtremo-opsz14wght900.ufo", name="RobotoExtremo-opsz14wght900.ufo", location=dict(wght=900, opsz=14), styleName="opsz14wght900", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-opsz18wght900.ufo", name="RobotoExtremo-opsz18wght900.ufo", location=dict(wght=900, opsz=18), styleName="opsz18wght900", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-opsz24wght100.ufo", name="RobotoExtremo-opsz24wght100.ufo", location=dict(wght=100, opsz=24), styleName="opsz24wght100", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-opsz24wght900.ufo", name="RobotoExtremo-opsz24wght900.ufo", location=dict(wght=900, opsz=24), styleName="opsz24wght900", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-opsz36wght100.ufo", name="RobotoExtremo-opsz36wght100.ufo", location=dict(wght=100, opsz=36), styleName="opsz36wght100", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-opsz36wght700.ufo", name="RobotoExtremo-opsz36wght700.ufo", location=dict(wght=700, opsz=36), styleName="opsz36wght900", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/RobotoExtremo-opsz36wght900.ufo", name="RobotoExtremo-opsz36wght900.ufo", location=dict(wght=900, opsz=36), styleName="opsz36wght900", familyName=familyName, copyInfo=False),


## Figures
	dict(path="master_ufo/RobotoExtremo-opsz18-wght100-wdth25.ufo", name="RobotoExtremo-opsz18-wght100-wdth25.ufo", location=dict(wght=100, opsz=18, wdth=25), styleName="opsz18-wght100-wdth25", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz24-wght100-wdth25.ufo", name="RobotoExtremo-opsz24-wght100-wdth25.ufo", location=dict(wght=100, opsz=24, wdth=25), styleName="opsz24-wght-100-wdth25", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz36-wght100-wdth25.ufo", name="RobotoExtremo-opsz36-wght100-wdth25.ufo", location=dict(wght=100, opsz=36, wdth=25), styleName="opsz36-wght100-wdth25", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz36-wght600-wdth25.ufo", name="RobotoExtremo-opsz36-wght600-wdth25.ufo", location=dict(wght=600, opsz=36, wdth=25), styleName="opsz36-wght600-wdth25", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz18-wght700-wdth25.ufo", name="RobotoExtremo-opsz18-wght700-wdth25.ufo", location=dict(wght=700, opsz=18, wdth=25), styleName="opsz18-wght700-wdth25", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz24-wght700-wdth25.ufo", name="RobotoExtremo-opsz24-wght700-wdth25.ufo", location=dict(wght=700, opsz=24, wdth=25), styleName="opsz24-wght700-wdth25", familyName=familyName, copyInfo=False),
	
	dict(path="master_ufo/RobotoExtremo-opsz24-wght100.ufo", name="RobotoExtremo-opsz24-wght100.ufo", location=dict(wght=100, opsz=24), styleName="opsz24-wght100", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz36-wght100.ufo", name="RobotoExtremo-opsz36-wght100.ufo", location=dict(wght=100, opsz=36), styleName="opsz36-wght100", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz18-wght700.ufo", name="RobotoExtremo-opsz18-wght700.ufo", location=dict(wght=700, opsz=18), styleName="opsz18-wght700", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz24-wght700.ufo", name="RobotoExtremo-opsz24-wght700.ufo", location=dict(wght=700, opsz=24), styleName="opsz24-wght700", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz36-wght700.ufo", name="RobotoExtremo-opsz36-wght700.ufo", location=dict(wght=700, opsz=36), styleName="opsz36-wght100", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz18-wght900.ufo", name="RobotoExtremo-opsz18-wght900.ufo", location=dict(wght=900, opsz=18), styleName="opsz18-wght900", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz24-wght900.ufo", name="RobotoExtremo-opsz24-wght900.ufo", location=dict(wght=900, opsz=24), styleName="opsz24-wght900", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz36-wght900.ufo", name="RobotoExtremo-opsz36-wght900.ufo", location=dict(wght=900, opsz=36), styleName="opsz36-wght900", familyName=familyName, copyInfo=False),
	
	
	dict(path="master_ufo/RobotoExtremo-opsz24-wght100-wdth151.ufo", name="RobotoExtremo-opsz24-wght100-wdth151.ufo", location=dict(wght=100, opsz=24, wdth=151), styleName="opsz24-wght100-wdth151", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz36-wght700-wdth151.ufo", name="RobotoExtremo-opsz36-wght700-wdth151.ufo", location=dict(wght=700, opsz=36, wdth=151), styleName="opsz36-wght700-wdth151", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz144-wght500-wdth151.ufo", name="RobotoExtremo-opsz144-wght500-wdth151.ufo", location=dict(wght=500, opsz=144, wdth=151), styleName="opsz144-wght500-wdth151", familyName=familyName, copyInfo=False),
	
##	NEW Caping
	
	dict(path="master_ufo/RobotoExtremo-opsz144-wght100-wdth25-GRAD-1.ufo", name="RobotoExtremo-opsz144-wght100-wdth25-GRAD-1.ufo", location=dict(wght=100, opsz=144, wdth=25, GRAD=-1), styleName="opsz144-wght100-wdth25-GRAD-1", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz144-wght100-wdth25-GRAD1.ufo", name="RobotoExtremo-opsz144-wght100-wdth25-GRAD1.ufo", location=dict(wght=100, opsz=144, wdth=25, GRAD=1), styleName="opsz144-wght100-wdth25-GRAD1", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz144-wght100-wdth151-GRAD-1.ufo", name="RobotoExtremo-opsz144-wght100-wdth151-GRAD-1.ufo", location=dict(wght=100, opsz=144, wdth=151, GRAD=-1), styleName="opsz144-wght100-wdth151-GRAD-1", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz144-wght100-wdth151-GRAD1.ufo", name="RobotoExtremo-opsz144-wght100-wdth151-GRAD1.ufo", location=dict(wght=100, opsz=144, wdth=151, GRAD=1), styleName="opsz144-wght100-wdth151-GRAD1", familyName=familyName, copyInfo=False),
	
	dict(path="master_ufo/RobotoExtremo-opsz144-wght100-GRAD1.ufo", name="RobotoExtremo-opsz144-wght100-GRAD1.ufo", location=dict(wght=100, opsz=144, GRAD=1), styleName="opsz144-wght100-GRAD1", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz144-wght100-GRAD-1.ufo", name="RobotoExtremo-opsz144-wght100-GRAD-1.ufo", location=dict(wght=100, opsz=144, GRAD=-1), styleName="opsz144-wght100-GRAD-1", familyName=familyName, copyInfo=False),
	
	dict(path="master_ufo/RobotoExtremo-opsz144-wght900-GRAD1.ufo", name="RobotoExtremo-opsz144-wght900-GRAD1.ufo", location=dict(wght=900, opsz=144, GRAD=1), styleName="opsz144-wght900-GRAD1", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz144-wght900-GRAD-1.ufo", name="RobotoExtremo-opsz144-wght900-GRAD-1.ufo", location=dict(wght=900, opsz=144, GRAD=-1), styleName="opsz144-wght900-GRAD-1", familyName=familyName, copyInfo=False),
	
	dict(path="master_ufo/RobotoExtremo-opsz144-wght900-wdth25-GRAD1.ufo", name="RobotoExtremo-opsz144-wght900-wdth25-GRAD1.ufo", location=dict(wght=900, opsz=144, wdth=25, GRAD=1), styleName="opsz144-wght900-wdth25-GRAD1", familyName=familyName, copyInfo=False),
	
	dict(path="master_ufo/RobotoExtremo-opsz8-wght100-GRAD-1.ufo", name="RobotoExtremo-opsz8-wght100-GRAD-1.ufo", location=dict(wght=100, opsz=8, GRAD=-1), styleName="opsz8-wght100-GRAD-1", familyName=familyName, copyInfo=False),
	

##	Caping & trimming instances github issue 56
# 	XOPQ27
	dict(path="master_ufo/RobotoExtremo-opsz8-wght100-wdth100-XOPQ27.ufo", name="RobotoExtremo-opsz8-wght100-wdth100-XOPQ27.ufo", location=dict(wght=100, opsz=8, wdth=100, XOPQ=27), styleName="opsz8-wght100-wdth100-XOPQ27", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz8-wght100-wdth25-XOPQ27.ufo", name="RobotoExtremo-opsz8-wght100-wdth25-XOPQ27.ufo", location=dict(wght=100, opsz=8, wdth=25, XOPQ=27), styleName="opsz8-wght100-wdth25-XOPQ27", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz8-wght100-wdth151-XOPQ27.ufo", name="RobotoExtremo-opsz8-wght100-wdth151-XOPQ27.ufo", location=dict(wght=100, opsz=8, wdth=151, XOPQ=27), styleName="opsz8-wght100-wdth151-XOPQ27", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz14-wght100-wdth100-XOPQ27.ufo", name="RobotoExtremo-opsz14-wght100-wdth100-XOPQ27.ufo", location=dict(wght=100, opsz=14, wdth=100, XOPQ=27), styleName="opsz14-wght100-wdth100-XOPQ27", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz14-wght100-wdth25-XOPQ27.ufo", name="RobotoExtremo-opsz14-wght100-wdth25-XOPQ27.ufo", location=dict(wght=100, opsz=14, wdth=25, XOPQ=27), styleName="opsz14-wght100-wdth25-XOPQ27", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz14-wght100-wdth151-XOPQ27.ufo", name="RobotoExtremo-opsz14-wght100-wdth151-XOPQ27.ufo", location=dict(wght=100, opsz=14, wdth=151, XOPQ=27), styleName="RobotoExtremo-opsz14-wght100-wdth151-XOPQ27", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz144-wght400-wdth100-XOPQ27.ufo", name="RobotoExtremo-opsz144-wght400-wdth100-XOPQ27.ufo", location=dict(wght=400, opsz=144, wdth=100, XOPQ=27), styleName="opsz144-wght400-wdth100-XOPQ27", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz144-wght100.ufo", name="RobotoExtremo-opsz144-wght100.ufo", location=dict(wght=100, opsz=144, wdth=100, XOPQ=27), styleName="opsz144-wght100", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz144-wght400-wdth25-XOPQ27.ufo", name="RobotoExtremo-opsz144-wght400-wdth25-XOPQ27.ufo", location=dict(wght=400, opsz=144, wdth=25, XOPQ=27), styleName="opsz144-wght400-wdth100-XOPQ27", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz144-wght100-wdth25.ufo", name="RobotoExtremo-opsz144-wght100-wdth25.ufo", location=dict(wght=100, opsz=144, wdth=25, XOPQ=27), styleName="opsz144-wght100-wdth25", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz144-wght900-wdth25-XOPQ27.ufo", name="RobotoExtremo-opsz144-wght900-wdth25-XOPQ27.ufo", location=dict(wght=900, opsz=144, wdth=25, XOPQ=27), styleName="opsz144-wght900-wdth25-XOPQ27", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz144-wght400-wdth151-XOPQ27.ufo", name="RobotoExtremo-opsz144-wght400-wdth151-XOPQ27.ufo", location=dict(wght=400, opsz=144, wdth=151, XOPQ=27), styleName="opsz144-wght400-wdth151-XOPQ27", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz144-wght100-wdth151.ufo", name="RobotoExtremo-opsz144-wght100-wdth151.ufo", location=dict(wght=100, opsz=144, wdth=151, XOPQ=27), styleName="opsz144-wght100-wdth151", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz144-wght900-wdth151-XOPQ27.ufo", name="RobotoExtremo-opsz144-wght900-wdth151-XOPQ27.ufo", location=dict(wght=900, opsz=144, wdth=151, XOPQ=27), styleName="opsz144-wght900-wdth151-XOPQ27", familyName=familyName, copyInfo=False),
 	
# 	#XOPQ175
	dict(path="master_ufo/RobotoExtremo-opsz144-wght400-wdth25-XOPQ175.ufo", name="RobotoExtremo-opsz144-wght400-wdth25-XOPQ175.ufo", location=dict(wght=400, opsz=144, wdth=25, XOPQ=175), styleName="opsz144-wght400-wdth25-XOPQ175", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz144-wght100-wdth25.ufo", name="RobotoExtremo-opsz144-wght100-wdth25.ufo", location=dict(wght=100, opsz=144, wdth=25, XOPQ=175), styleName="opsz144-wght100-wdth25", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz144-wght900-wdth25-XOPQ175.ufo", name="RobotoExtremo-opsz144-wght900-wdth25-XOPQ175.ufo", location=dict(wght=900, opsz=144, wdth=25, XOPQ=175), styleName="opsz144-wght900-wdth25-XOPQ175", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz144-wght900-wdth151-XOPQ175.ufo", name="RobotoExtremo-opsz144-wght900-wdth151-XOPQ175.ufo", location=dict(wght=900, opsz=144, wdth=151, XOPQ=175), styleName="opsz144-wght900-wdth151-XOPQ175", familyName=familyName, copyInfo=False),
 	
# 	#YOPQ25
	dict(path="master_ufo/RobotoExtremo-opsz8-wght100-wdth100-YOPQ25.ufo", name="RobotoExtremo-opsz8-wght100-wdth100-YOPQ25.ufo", location=dict(wght=100, opsz=8, wdth=100, YOPQ=25), styleName="opsz8-wght100-wdth100-YOPQ25", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz8-wght100-wdth25-YOPQ25.ufo", name="RobotoExtremo-opsz8-wght100-wdth25-YOPQ25.ufo", location=dict(wght=100, opsz=8, wdth=25, YOPQ=25), styleName="opsz8-wght100-wdth25-YOPQ25", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz8-wght100-wdth151-YOPQ25.ufo", name="RobotoExtremo-opsz8-wght100-wdth151-YOPQ25.ufo", location=dict(wght=100, opsz=8, wdth=151, YOPQ=25), styleName="opsz8-wght100-wdth151-YOPQ25", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz14-wght100-wdth100-YOPQ25.ufo", name="RobotoExtremo-opsz14-wght100-wdth100-YOPQ25.ufo", location=dict(wght=100, opsz=14, wdth=100, YOPQ=25), styleName="opsz14-wght100-wdth100-YOPQ25", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz14-wght100-wdth25-YOPQ25.ufo", name="RobotoExtremo-opsz14-wght100-wdth25-YOPQ25.ufo", location=dict(wght=100, opsz=14, wdth=25, YOPQ=25), styleName="opsz14-wght100-wdth25-YOPQ25", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz14-wght100-wdth151-YOPQ25.ufo", name="RobotoExtremo-opsz14-wght100-wdth151-YOPQ25.ufo", location=dict(wght=100, opsz=14, wdth=151, YOPQ=25), styleName="opsz14-wght100-wdth151-YOPQ25", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz144-wght400-wdth100-YOPQ25.ufo", name="RobotoExtremo-opsz144-wght400-wdth100-YOPQ25.ufo", location=dict(wght=400, opsz=144, wdth=100, YOPQ=25), styleName="opsz144-wght400-wdth100-YOPQ25", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz144-wght100.ufo", name="RobotoExtremo-opsz144-wght100.ufo", location=dict(wght=100, opsz=144, YOPQ=25), styleName="opsz144-wght100", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz144-wght400-wdth25-YOPQ25.ufo", name="RobotoExtremo-opsz144-wght400-wdth25-YOPQ25.ufo", location=dict(wght=400, opsz=144, wdth=25, YOPQ=25), styleName="opsz144-wght400-wdth25-YOPQ25", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz144-wght100-wdth25.ufo", name="RobotoExtremo-opsz144-wght100-wdth25.ufo", location=dict(wght=100, opsz=144, wdth=25, YOPQ=25), styleName="opsz144-wght100-wdth25", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz144-wght400-wdth151-YOPQ25.ufo", name="RobotoExtremo-opsz144-wght400-wdth151-YOPQ25.ufo", location=dict(wght=400, opsz=144, wdth=151, YOPQ=25), styleName="opsz144-wght400-wdth151-YOPQ25", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz144-wght100-wdth151.ufo", name="RobotoExtremo-opsz144-wght100-wdth151.ufo", location=dict(wght=100, opsz=144, wdth=151, YOPQ=25), styleName="opsz144-wght100-wdth151", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz144-wght900-wdth151-YOPQ25.ufo", name="RobotoExtremo-opsz144-wght900-wdth151-YOPQ25.ufo", location=dict(wght=900, opsz=144, wdth=151, YOPQ=25), styleName="opsz144-wght900-wdth151-YOPQ25", familyName=familyName, copyInfo=False),
 	
# 	#YOPQ135
	dict(path="master_ufo/RobotoExtremo-opsz144-wght900-wdth100-YOPQ135.ufo", name="RobotoExtremo-opsz144-wght900-wdth100-YOPQ135.ufo", location=dict(wght=900, opsz=144, wdth=100, YOPQ=135), styleName="opsz144-wght900-wdth100-YOPQ135", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz144-wght400-wdth25-YOPQ135.ufo", name="RobotoExtremo-opsz144-wght400-wdth25-YOPQ135.ufo", location=dict(wght=400, opsz=144, wdth=25, YOPQ=135), styleName="opsz144-wght400-wdth25-YOPQ135", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz144-wght100-wdth25.ufo", name="RobotoExtremo-opsz144-wght100-wdth25.ufo", location=dict(wght=100, opsz=144, wdth=25, YOPQ=135), styleName="opsz144-wght100-wdth25", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz144-wght900-wdth25-YOPQ135.ufo", name="RobotoExtremo-opsz144-wght900-wdth25-YOPQ135.ufo", location=dict(wght=900, opsz=144, wdth=25, YOPQ=135), styleName="opsz144-wght900-wdth25-YOPQ135", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz144-wght900-wdth151-YOPQ135.ufo", name="RobotoExtremo-opsz144-wght900-wdth151-YOPQ135.ufo", location=dict(wght=900, opsz=144, wdth=151, YOPQ=135), styleName="opsz144-wght900-wdth151-YOPQ135", familyName=familyName, copyInfo=False),

#  	#XTRA323
	dict(path="master_ufo/RobotoExtremo-opsz8-wght900-wdth25-XTRA323.ufo", name="RobotoExtremo-opsz8-wght900-wdth25-XTRA323.ufo", location=dict(wght=900, opsz=8, wdth=25, XTRA=323), styleName="opsz8-wght900-wdth25-XTRA323", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz14-wght900-wdth100-XTRA323.ufo", name="RobotoExtremo-opsz14-wght900-wdth100-XTRA323.ufo", location=dict(wght=900, opsz=14, wdth=100, XTRA=323), styleName="opsz14-wght900-wdth100-XTRA323", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz14-wght900-wdth25-XTRA323.ufo", name="RobotoExtremo-opsz14-wght900-wdth25-XTRA323.ufo", location=dict(wght=900, opsz=14, wdth=25, XTRA=323), styleName="opsz14-wght900-wdth25-XTRA323", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz144-wght100.ufo", name="RobotoExtremo-opsz144-wght100.ufo", location=dict(wght=100, opsz=144, wdth=100, XTRA=323), styleName="opsz144-wght100", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz144-wght900-wdth100-XTRA323.ufo", name="RobotoExtremo-opsz144-wght900-wdth100-XTRA323.ufo", location=dict(wght=900, opsz=144, wdth=100, XTRA=323), styleName="opsz144-wght900-wdth100-XTRA323", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz144-wdth25.ufo", name="RobotoExtremo-opsz144-wdth25.ufo", location=dict(wght=400, opsz=144, wdth=25, XTRA=323), styleName="opsz144-wdth25", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz144-wght100-wdth25.ufo", name="RobotoExtremo-opsz144-wght100-wdth25.ufo", location=dict(wght=100, opsz=144, wdth=25, XTRA=323), styleName="opsz144-wght100-wdth25", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz144-wght900-wdth25.ufo", name="RobotoExtremo-opsz144-wght900-wdth25.ufo", location=dict(wght=900, opsz=144, wdth=25, XTRA=323), styleName="opsz144-wght900-wdth25", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz144-wght400-wdth100-XTRA323.ufo", name="RobotoExtremo-opsz144-wght400-wdth100-XTRA323.ufo", location=dict(wght=400, opsz=144, wdth=100, XTRA=323), styleName="opsz144-wght400-wdth100-XTRA323", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz144-wght100-wdth151.ufo", name="RobotoExtremo-opsz144-wght100-wdth151.ufo", location=dict(wght=100, opsz=144, wdth=151, XTRA=323), styleName="opsz144-wght900-wdth25", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz144-wght400-wdth151-XTRA323.ufo", name="RobotoExtremo-opsz144-wght400-wdth151-XTRA323.ufo", location=dict(wght=400, opsz=144, wdth=151, XTRA=323), styleName="opsz144-wght400-wdth151-XTRA323", familyName=familyName, copyInfo=False),

#  	#XTRA603
	dict(path="master_ufo/RobotoExtremo-opsz144-wght400-wdth100-XTRA603.ufo", name="RobotoExtremo-opsz144-wght400-wdth100-XTRA603.ufo", location=dict(wght=400, opsz=144, wdth=100, XTRA=603), styleName="opsz144-wght400-wdth100-XTRA603", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz144-wght100-wdth100-XTRA603.ufo", name="RobotoExtremo-opsz144-wght100-wdth100-XTRA603.ufo", location=dict(wght=100, opsz=144, wdth=100, XTRA=603), styleName="opsz144-wght100-wdth100-XTRA603", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz144-wght400-wdth25-XTRA603.ufo", name="RobotoExtremo-opsz144-wght400-wdth25-XTRA603.ufo", location=dict(wght=400, opsz=144, wdth=25, XTRA=603), styleName="opsz144-wght400-wdth25-XTRA603", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz144-wght100-wdth25.ufo", name="RobotoExtremo-opsz144-wght100-wdth25.ufo", location=dict(wght=100, opsz=144, wdth=25, XTRA=603), styleName="opsz144-wght100-wdth25", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz144-wght900-wdth25-XTRA603.ufo", name="RobotoExtremo-opsz144-wght900-wdth25-XTRA603.ufo", location=dict(wght=900, opsz=144, wdth=25, XTRA=603), styleName="opsz144-wght900-wdth25-XTRA603", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/RobotoExtremo-opsz144-wght100-wdth151-XTRA603.ufo", name="RobotoExtremo-opsz144-wght100-wdth151-XTRA603.ufo", location=dict(wght=100, opsz=144, wdth=151, XTRA=603), styleName="opsz144-wght100-wdth151-XTRA603", familyName=familyName, copyInfo=False),
	
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
	dict(minimum=416, maximum=570, default=514, name="YTLC", tag="YTLC", labelNames={"en": "YTLC"}, map=[]),
	dict(minimum=528, maximum=760, default=712, name="YTUC", tag="YTUC", labelNames={"en": "YTUC"}, map=[]),
	dict(minimum=649, maximum=854, default=750, name="YTAS", tag="YTAS", labelNames={"en": "YTAS"}, map=[]),
	dict(minimum=-305, maximum=-98, default=-203, name="YTDE", tag="YTDE", labelNames={"en": "YTDE"}, map=[]),
#	dict(minimum=560, maximum=788, default=738, name="YTFI", tag="YTFI", labelNames={"en": "YTFI"}, map=[]),
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
	if fileName not in ['RobotoExtremo-opsz144.ufo', 'RobotoExtremo-wght100.ufo', 'RobotoExtremo-wght900.ufo', 'RobotoExtremo-wdth151.ufo', 'RobotoExtremo-wdth25.ufo']:
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

# Remove temporary 1-drawings
if os.path.exists("sources/1-drawings"):
	shutil.rmtree("sources/1-drawings", ignore_errors=True)

print ("DONE!")

# SUBSET COMMAND
# pyftsubset RobotoExtremo-VF.ttf --text-file=ascii-subset.txt --output-file=RobotoExtremo-subset-VF.ttf
