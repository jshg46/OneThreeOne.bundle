######################################################################################
#
#	Channel 131 - v0.10
#
######################################################################################

TITLE = "Channel 131"
PREFIX = "/video/onethreeone"
ART = "art-default.jpg"
ICON = "icon-default.png"
ICON_SERIES = "icon-tv.png"
BASE_URL = "http://chan131.so"

######################################################################################
# Set global variables

def Start():

	ObjectContainer.title1 = TITLE
	ObjectContainer.art = R(ART)
	DirectoryObject.thumb = R(ICON_SERIES)
	DirectoryObject.art = R(ART)
	VideoClipObject.thumb = R(ICON_SERIES)
	VideoClipObject.art = R(ART)

	HTTP.Headers['Accept'] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
	HTTP.Headers['Accept-Encoding'] = "gzip, deflate"
	HTTP.Headers['Accept-Language'] = "en-US,en;q=0.5"
	HTTP.Headers['Cache-Control'] = "max-age=0"
	HTTP.Headers['Connection'] = "keep-alive"
	HTTP.Headers['Cookie'] = "__cfduid=d345202ed3eb4cc8194e92f763bba86511426283176"
	HTTP.Headers['DNT'] = "1"
	HTTP.Headers['Host'] = "chan131.so"
	HTTP.Headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1; rv:35.0.1) Gecko/20100101 Firefox/35.0.1 anonymized by Abelssoft 1584666243"
	
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
		title = each.xpath("./a/text()")[0]
		url = each.xpath("./a/@href")[0]
		oc.add(DirectoryObject(
			key = Callback(ShowEpisodes, title = title, url = url),
				title = title,
				thumb = ICON_SERIES
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
				thumb = ICON_SERIES
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
		thumb = thumb,
		url = url
		)
	)	
	
	return oc	
