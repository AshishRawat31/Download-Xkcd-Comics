#! python3
# DownloadComics.py - Download every single XKCD.com comic.

import requests, os, bs4

url = 'http://xkcd.com' #starting URL
os.makedirs('xkcd', exist_ok=True) #store comics in ./xkcd

while not url.endswith('#'):
	#Download the page
    print('Downloading.......')
    res = requests.get(url)
    try:
        res.raise_for_status()
    except Exception as exc:
        print('This is a problem: %s' % (exc))
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    #Find the URL of comic image
    comicElem = soup.select('#comic img')
    if comicElem == []:
        print('Could not find comic image.')
    else:
        try:
            comicUrl = 'http:' + comicElem[0].get('src')
            print('Downloading image %s...' % (comicUrl))
            res = requests.get(comicUrl)
            try:
                res.raise_for_status()
            except Exception as exc:
                print('This is a problem: %s' % (exc))
        except requests.exceptions.MissingSchema:
			#skip this comic
            prevLink = soup.select('a[rel="prev"]')[0]
            url = 'http://xkcd.com' + prevLink.get('href')
            continue
	#Save the image to ./xkcd
    imageFile = open(os.path.join('xkcd', os.path.basename(comicUrl)), 'wb')	
    for chunk in res.iter_content():
        imageFile.write(chunk)
    imageFile.close()

	#Get the prev button's url.
    prevLink = soup.select('a[rel="prev"]')[0]
    url='http://xkcd.com' + prevLink.get('href')

print('Done.')
