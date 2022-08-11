import argparse
import logging
import os
from unicodedata import name
from dotenv import load_dotenv
import sys
import pprint

from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

logger = logging.getLogger('examples.artist_albums')
logging.basicConfig(level='INFO')

''' sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials()) '''

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID,
                                                           client_secret=CLIENT_SECRET))


def get_args():
    parser = argparse.ArgumentParser(description='Gets albums from artist')
    parser.add_argument('-a', '--artist', required=True,
                        help='Name of Artist')
    return parser.parse_args()


def get_artist(name):
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        print(items[0]['id'])
        return items[0]
        
    else:
        return None


def show_artist_albums(artist):
    albums = []
    results = sp.artist_albums(artist['id'], album_type='album')
    albums.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])
    seen = set()  # to avoid dups
    albums.sort(key=lambda album: album['name'].lower())
    for album in albums:
        name = album['name']
        if name not in seen:
            logger.info('ALBUM: %s', name)
            seen.add(name)


def main():
    ''' args = get_args()
    artist = get_artist(args.artist)
    print('spotify:artist:' + artist["id"])
    if artist:
        show_artist_albums(artist)
    else:
        logger.error("Can't find artist: %s", artist) '''

    ''' artist = get_artist(sys.argv[1])
    artist_id = 'spotify:artist:' + artist["id"]

   
    response = sp.artist_top_tracks(artist_id)

    for track in response['tracks']:
        print(track['name']) '''
    
    '''  '''
    ''' val = sys.argv[1:len(sys.argv)] '''
    ##############################################
    ''' val1 = input ("Enter Album Name :")
    val2 = input ("Enter Artist Name :")
    result = sp.search(q='album: '+ str(val1) + ' artist: ' + val2, type='album', limit='1') '''
    ###############################################
    result = sp.search(q='album: '+str(sys.argv[1:]), type='album', limit='1')


    album_artist = result['albums']['items'][0]['artists'][0]['name']
    
    album_uri = result['albums']['items'][0]['uri']

    pprint.pprint(album_uri);
    

    result2 = sp.search(q='artist: ' + album_artist, type='artist', limit='1')
    pprint.pprint(result2)


    album_info = sp.album(album_uri)
    pprint.pprint(album_info['tracks']['items'][4])

    for i in album_info['tracks']['items']:
        print("Track Number: ", i['track_number'])
        print("Track Name: ", i['name'])
        print()


''' client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

if len(sys.argv) > 1:
    artist_name = ' '.join(sys.argv[1:])
    results = sp.search(q=artist_name, limit=20)
    for i, t in enumerate(results['tracks']['items']):
        print(' ', i, t['name'])
 '''

if __name__ == '__main__':
    main()
