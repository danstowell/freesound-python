import os.path
import json

from freesound import Freesound, Sound
from localdata import freesound_api_key
Freesound.set_api_key(freesound_api_key)

##################################
# settings:
tagsearch = "field-recording"
outfolder = 'soundsgot'
maxpages = 3
audiotype = "wav"
minduration = 10

##################################
# let's go
fquery = "tag:%s type:%s duration:[%g TO *]" % (tagsearch, audiotype, minduration)
print fquery
pager = Sound.search(f=fquery)

print pager.keys()
print "Num results: %i" % pager['num_results']
print "Num pages  : %i" % pager['num_pages'  ]

for whichpage in range(min(maxpages, pager['num_pages'])):
	print "----- PAGE %i -----" % (whichpage + 1)
	for s in pager['sounds']:
		thesound = Sound.get_sound(s['id'])
		print "%i %s %s" % (s['id'], s['original_filename'], s['url'])
		outfname = "%i.%s" % (s['id'], audiotype)
		if os.path.isfile("%s/%s" % (outfolder, outfname)):
			print "           already got"
		else:
			thesound.retrieve(outfolder, outfname)
			# we also write metadata to file
			jsonf = open("%s/%i.json" % (outfolder, s['id']), 'w')
			# we can't serialise the object directly, so add some of its keys to the search result which we'll serialise
			for key in ['license', 'samplerate', 'channels', 'geotag']:
				try:
					s[key] = thesound[key]
				except:
					pass
			jsonf.write(json.dumps(s))
			jsonf.close()

	print
	pager.next()

print "Done."

