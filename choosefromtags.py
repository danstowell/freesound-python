import glob, json
import numpy as np

#ffpath = '/home/dan/freefield1010_v02'
ffpath = './5mins/01'

taggroups = {
 'weather': [u'weather', u'wind', u'rain', u'storm', u'thunderstorm'],
 'voices': [u'crowd', u'human', u'people', u'talking', u'voice', u'voices', u'speech'],
 'outdoor': [u'outdoor', u'outdoors', u'park'],
 'waterway': [u'stream', u'river', u'waves', u'sea'],
 'woodland': [u'forest', u'birds', u'birdsong'],
}

counts = {k:0 for k in taggroups.keys()}
for onepath in glob.iglob("%s/*.json" % ffpath):
	jsonfile = open(onepath, 'r')
	jsondata = json.load(jsonfile)
	jsonfile.close()
	thetags = jsondata.get(u'tags')
	curcounts = {k:0 for k in taggroups.keys()}
	for gkey, glist in taggroups.items():
		if any([posstag in thetags for posstag in glist]):
			curcounts[gkey] += 1
	if np.sum(curcounts.values()) == 1:  # ignore any that land in multiple categories
		for gkey, glist in taggroups.items():
			counts[gkey] += curcounts[gkey]

print counts

