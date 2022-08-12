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

def fetch_spotify_info():
    ##############################################
    ''' val1 = input ("Enter Album Name :")
    val2 = input ("Enter Artist Name :")
    result = sp.search(q='album: '+ str(val1) + ' artist: ' + val2, type='album', limit='1') '''
    ###############################################
    result = sp.search(q='album: '+str(sys.argv[1:]), type='album', limit='1')

    ##  Getting Album 'id' from search results

    album_uri = result['albums']['items'][0]['uri']
    pprint.pprint(album_uri);
    
    #########   Getting artist info   ###############

    album_artist = result['albums']['items'][0]['artists'][0]['name']
    result2 = sp.search(q='artist: ' + album_artist, type='artist', limit='1')
    pprint.pprint(result2)

    print("Artist Info")
    print()

    print(result2['artists']['items'][0]['images'][1]['url'])
    print(result2['artists']['items'][0]['name'])


    #########   Getting Album info   ###############

    ##  General info

    album_info = sp.album(album_uri)
    #pprint.pprint(album_info)
    #pprint.pprint(album_info['tracks']['items'])

    print()
    print()
    print("Album INFO")
    print()

    print(album_info['name'])
    print(album_info['album_type'])
    print(album_info['label'])
    print(album_info['release_date'])
    print(album_info['total_tracks'])
    print(album_info['popularity'])
    popularity = album_info['popularity']
   
    show_popularity(popularity)

    
    

    print()
    print()


    ##  Getting track info  

    print("TRACK INFO")
    print()

    m = 0

    for i in album_info['tracks']['items']:
        
        print("Track Number: ", i['track_number'])
        print("Track Name: ", i['name'])
        
        for j in album_info['tracks']['items'][m]['artists']:
            print("artists involved:", j['name'])
            
        #print("artists involved:", i['artists'][0]['name'])
        print()
        m+=1

def show_popularity(popularity):
    print()
    print("  POPULARITY RATING: ", popularity)
    print()
    if popularity < 20:
        print("*")
    elif popularity > 19 and popularity < 40:
        print("* *")
    elif popularity > 39 and popularity < 60:
        print("* * *")
    elif popularity > 59 and popularity < 80:
        print("* * * *")
    elif popularity > 79 and popularity < 100:
        print("* * * * *")
    
        


def main():
    fetch_spotify_info()
    

if __name__ == '__main__':
    main()
