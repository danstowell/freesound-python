import os.path

from freesound.__init__ import Freesound, Sound
from localdata import freesound_api_key
Freesound.set_api_key(freesound_api_key)

##################################
# settings:
tagsearch = "field-recording"
maxpages = 3
audiotype = "wav"

##################################
# let's go
#pager = Sound.search(q=tagsearch)
pager = Sound.search(f="tag:%s type:%s" % (tagsearch, audiotype))

print pager.keys()
print "Num results: %i" % pager['num_results']
print "Num pages  : %i" % pager['num_pages'  ]

for whichpage in range(min(maxpages, pager['num_pages'])):
	print "----- PAGE %i -----" % (whichpage + 1)
	for s in pager['sounds']:
		thesound = Sound.get_sound(s['id'])
#		print "%i " % s['id'],
#		print s.keys()
		print "%i %s %s" % (s['id'], s['original_filename'], s['url'])
		outpath = "%i.%s" % (s['id'], audiotype)
		if os.path.isfile("soundsgot/%s" % outpath):
			print "           already got"
		else:
			thesound.retrieve('soundsgot', outpath)
			# TODO at this point also write metadata to file
	print
	pager.next()


"""
# Get sound info example
print "Sound info:"
print "-----------"
s = Sound.get_sound(96541)
print "Getting sound: " + s['original_filename']
print "Url: " + s['url']
print "Description: " + s['description']
print "Tags: " + str(s['tags'])
print "\n"
"""

