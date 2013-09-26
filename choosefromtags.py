import glob, json
import numpy as np
import shutil, random, os

#ffpath = '/home/dan/freefield1010_v02'
ffpath = './5mins/01'

outdir = 'thematic'

taggroups = {
 'weather': [u'weather', u'wind', u'rain', u'storm', u'thunderstorm'],
 'voices': [u'crowd', u'human', u'people', u'talking', u'voice', u'voices', u'speech'],
 'outdoor': [u'outdoor', u'outdoors', u'park'],
 'waterway': [u'stream', u'river', u'waves', u'sea'],
 'woodland': [u'forest', u'birds', u'birdsong'],
}

############################################################
def mkdir_p(path):
        try:
                os.makedirs(path)
        except OSError as exc: # Python >2.5
                if exc.errno == errno.EEXIST: pass
                else: raise

############################################################
ids = {k:[] for k in taggroups.keys()}
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
			if curcounts[gkey]:
				ids[gkey].append(jsondata.get(u'id'))

random.seed(97867564) # this is to make the shuffle repeatable

for k,someids in ids.items():
	print "===================================================="
	print k
	for itemid in someids:
		print "%s" % itemid
	thisoutdir = "%s/%s" % (outdir, k)
	mkdir_p(thisoutdir)
	random.shuffle(someids)
	for itemid in someids[:10]:
		shutil.copyfile("%s/%s.json" % (ffpath, itemid), "%s/%s.json" % (thisoutdir, itemid))
		shutil.copyfile("%s/%s.wav"  % (ffpath, itemid), "%s/%s.wav"  % (thisoutdir, itemid))


print {k:len(someids) for k,someids in ids.items()}

