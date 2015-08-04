import requests
from models import Torrent
from utils.utils import utils

def search(query):
	search_url="https://getstrike.net/api/v2/torrents/search/?phrase=%s&category=Movies" %query
	data=requests.get(search_url).json()
	torrents=[]
	for result in data["torrents"]:
		t=Torrent()
		t.title=result['torrent_title']
		t.seeds=result['seeds']
		t.size=utils.hsize(result['size'])
		t.torrent_url=result['magnet_uri']
		torrents.append(t)
	return torrents
