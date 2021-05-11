from __future__ import print_function, division, unicode_literals
import glob, json, io, re, os, sys
from fontTools.ttLib import TTFont
from datetime import datetime, timedelta
from collections import OrderedDict

infiles = "fonts/repos/*/fonts/*.?tf"
outdir = "fonts"
fileAxes = {}

def getName(ttf, nameid):
    names = [n for n in ttf['name'].names if n.nameID==nameid]
    return names[0].toUnicode()

def getVarAxes(ttf):
    axes = OrderedDict()
    if 'STAT' in ttf and hasattr(ttf['STAT'], 'table'):
        axes['order'] = [a.AxisTag for a in sorted(ttf['STAT'].table.DesignAxisRecord.Axis, key=lambda a:a.AxisOrdering)]

    if 'fvar' in ttf:
        for axis in ttf['fvar'].axes:
            axes[axis.axisTag] = {
                'name': getName(ttf, axis.nameID if hasattr(axis, 'nameID') else axis.axisNameID),
                'min': axis.minValue,
                'max': axis.maxValue,
                'default': axis.defaultValue
            }
        axes['instances'] = []
        if hasattr(ttf['fvar'], 'instances'):
            for instance in ttf['fvar'].instances:
                axes['instances'].append({
                    'axes': instance.coordinates,
                    'name': getName(ttf, instance.nameID if hasattr(instance, 'nameID') else instance.subfamilyNameID),
                })
    return axes

for fontfile in glob.glob(infiles):
    fontfilebase = os.path.basename(fontfile)[:-4]
    outbase = os.path.join(outdir, fontfilebase)

    ttf = TTFont(fontfile, recalcBBoxes=False)

    #list axes
    fileAxes[fontfilebase] = getVarAxes(ttf)

    if 'DSIG' in ttf:
        del(ttf['DSIG'])

    wofffile = outbase + ".woff"
    ttf.flavor = 'woff'
    ttf.save(wofffile)

#using binary here because json.dumps returns raw bytes
with io.open(os.path.join(outdir, 'axes.json'), 'wb') as axesfile:
    jsonbytes = json.dumps(fileAxes, indent=2, ensure_ascii=False)
    if not isinstance(jsonbytes, bytes):
        jsonbytes = jsonbytes.encode('utf-8')
    axesfile.write(jsonbytes)

sys.exit(0)
