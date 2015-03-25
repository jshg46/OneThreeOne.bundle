######################################################################################
#
#	Channel 131 - v0.10
#
######################################################################################

TITLE = "Channel 131"
PREFIX = "/video/onethreeone"
ART = "art-default.jpg"
ICON = "icon-default.png"
ICON_MOVIES = "icon-tv.png"
ICON_LIST = "icon-list.png"
BASE_URL = "http://chan131.so"

######################################################################################
# Set global variables

def Start():

	ObjectContainer.title1 = TITLE
	ObjectContainer.art = R(ART)
	DirectoryObject.thumb = R(ICON_LIST)
	DirectoryObject.art = R(ART)
	VideoClipObject.thumb = R(ICON_MOVIES)
	VideoClipObject.art = R(ART)

	HTTP.CacheTime = CACHE_1HOUR
<<<<<<< HEAD
	HTTP.Headers['User-Agent'] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36"
	HTTP.Headers['Accept'] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
=======
	HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'
>>>>>>> origin/master
	HTTP.Headers['Host'] = "chan131.so"
	
######################################################################################
# Menu hierarchy

@handler(PREFIX, TITLE, art=ART, thumb=ICON)
def MainMenu():

	return Shows()

######################################################################################
# Creates page url from category and creates objects from that page

@route(PREFIX + "/shows")	
def Shows():

	oc = ObjectContainer()
	html = HTML.ElementFromURL(BASE_URL + '/tv-shows')

	for each in html.xpath("//div[@class='recent']/ul/li"):
		try:
			title = each.xpath("./a/text()")[0]
			url = each.xpath("./a/@href")[0]
			thumb = url
		except:
			title = ""
			url = ""
			thumb = ""

		oc.add(DirectoryObject(
			key = Callback(ShowEpisodes, title = title, url = url),
				title = title,
				thumb = Resource.ContentsOfURLWithFallback(url = thumb, fallback='icon-tv.png')
				)
		)
	return oc

######################################################################################
@route(PREFIX + "/showepisodes")	
def ShowEpisodes(title, url):

	oc = ObjectContainer(title1 = title)
	html = HTML.ElementFromURL(url)

	for each in html.xpath("//div[@class='recent']/ul/li"):
		title = each.xpath("./a/text()")[0]
		url = each.xpath("./a/@href")[0]
		thumb = url
		oc.add(DirectoryObject(
			key = Callback(EpisodeDetail, title = title, url = url),
				title = title,
				thumb = 'icon-tv.png'
				)
		)
	return oc

######################################################################################
@route(PREFIX + "/episodedetail")
def EpisodeDetail(title, url):
	
	oc = ObjectContainer(title1 = title)
	page = HTML.ElementFromURL(url)
	title = page.xpath("//div[@class='most-recent']/h2[1]/text()")[0]
	try:
		description = page.xpath("//p[@class='description']/text()")[0]
	except:
		description = ""
	thumb = url

	oc.add(VideoClipObject(
		title = title,
		summary = description,
		thumb = Resource.ContentsOfURLWithFallback(url = thumb, fallback='icon-tv.png'),
		url = url
		)
	)	
	
	return oc	
