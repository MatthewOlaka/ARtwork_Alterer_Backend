import argparse
import logging
import os
from unicodedata import name
from dotenv import load_dotenv
import sys
import pprint
from PIL import Image, ImageDraw, ImageFont
from colorthief import ColorThief
import math
import numpy as np


from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import urllib.request


load_dotenv()

''' tracks_dict = dict()
track_artist_dict = dict() '''
tracks_dict = {}
track_artist_dict = {}


CLIENT_ID = os.getenv('CLIENT_ID') 
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

logger = logging.getLogger('examples.artist_albums')
logging.basicConfig(level='INFO')

''' sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials()) '''

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID,
                                                           client_secret=CLIENT_SECRET))

                                        
def isLightOrDark(rgbColor):
    [r,g,b]=rgbColor
    hsp = math.sqrt(0.299 * (r * r) + 0.587 * (g * g) + 0.114 * (b * b))
    if (hsp>127.5):
        return 'light'
    else:
        return 'dark' 


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
    artist_uri = result['albums']['items'][0]['artists'][0]['uri']
    #result2 = sp.search(q='artist: ' + album_artist, type='artist', limit='1')
    #pprint.pprint(result)

    print("Artist Info")
    print()

    artist_info = sp.artist(artist_uri)
    pprint.pprint(artist_info)

    #artist_name = result2['artists']['items'][0]['name']
    #artist_img_url = result2['artists']['items'][0]['images'][1]['url']

    artist_name = artist_info['name']
    artist_img_url = artist_info['images'][1]['url']



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
    album_name = album_info['name']
    print(album_info['album_type'])
    project_type = album_info['album_type']
    print(album_info['label'])
    label = album_info['label']
    print(album_info['release_date'])
    release_date = album_info['release_date']
    print(album_info['total_tracks'])
    total_tracks = album_info['total_tracks']
    print(album_info['popularity'])
    popularity = album_info['popularity']
    #print(album_info['duration_ms'])
    #duration = album_info['duration_ms']

   
    show_popularity(popularity)

    #pprint.pprint(album_info)
    print()
    print()


    ##  Getting track info  

    print("TRACK INFO")
    print()

    m = 0

    for i in album_info['tracks']['items']:
        
        print("Track Number: ", i['track_number'])
        print("Track Name: ", i['name'])
        tracks_dict[i['track_number']] = i['name']

        artist_arr = []
        
        for j in album_info['tracks']['items'][m]['artists']:
            print("artists involved:", j['name'])
            artist_arr.append(j['name'])
            track_artist_dict[i['track_number']] = artist_arr
            
        #print("artists involved:", i['artists'][0]['name'])
        print()
        m+=1
    
    print("yeye$%$#@#$%$#$%$#$%$#$")
    print(tracks_dict)
    print()
    print(track_artist_dict)
    print("yeye$%$#@#$%$#$%$#$%$#$")

    
    # Creating the Image

    make_image(artist_name, artist_img_url, album_name, label, project_type, release_date, total_tracks, popularity)

def make_image(artist_name, artist_url, album_name, label, project_type, release_date, total_tracks, popularity):

    #font = ImageFont.load("arial.pil")

    urllib.request.urlretrieve(artist_url, artist_name + "_AR.png")
  
    img = Image.open(artist_name + "_AR.png")
    star = Image.open('images/star2.png')

    empty_star = Image.open('images/emptystar.png')

    #Get Dominant Color from spotify's artist picture

    color_thief = ColorThief(artist_name + "_AR.png")
    dominant_color = color_thief.get_color(quality=1)
    print("Dominant color: ",dominant_color)

    arr = np.asarray(dominant_color)
    fla_color_arr = arr.flatten()
    print(fla_color_arr)

    #isLightOrDark(fla_color_arr)

    

    new = Image.new('RGB', (900,900), color=dominant_color)

    new.paste(img,(550,30))

    #d = ImageDraw.Draw(new)
    #d.text((100, 100), artist_name, fill=(0,0,0))

    draw = ImageDraw.Draw(new)
    # use a bitmap font
    
    title_font = ImageFont.truetype("Sora.ttf", 45)
    h2_font = ImageFont.truetype("Sora.ttf", 35)
    h3_font = ImageFont.truetype("Sora.ttf", 20)
    track_font = ImageFont.truetype("Sora.ttf", 25)
    feature_font = ImageFont.truetype("Sora.ttf", 15)
    row_space1 = 0
    row_space2 = 0

    #column 2
    row_space3 = 0
    row_space4 = 0


    if isLightOrDark(fla_color_arr) == 'dark':
        
        draw.text((550, 360), artist_name, font=h3_font, fill=(255,255,255))
        draw.text((20, 30), album_name, font=title_font, fill=(255,255,255))
        draw.text((20, 100), label, font=h3_font, fill=(255,255,255))
        draw.text((20, 140), str(project_type).capitalize(), font=h3_font, fill=(255,255,255))
        draw.text((100, 145), "°", font=h3_font, fill=(255,255,255))
        draw.text((120, 140), release_date, font=h3_font, fill=(255,255,255))
        if total_tracks > 1:
            
            draw.text((20, 180), str(total_tracks) + " tracks", font=h3_font, fill=(255,255,255))
            draw.text((120, 185), "°", font=h3_font, fill=(255,255,255))
            #draw.text((150, 185), duration, font=h3_font, fill=(255,255,255))
        else: 
            draw.text((20, 180), str(total_tracks) + " track", font=h3_font, fill=(255,255,255))
            draw.text((100, 185), "°", font=h3_font, fill=(255,255,255))
            #draw.text((150, 185), duration, font=h3_font, fill=(255,255,255))

        draw.text((120, 210), "Popularity Rating:", font=h2_font, fill=(255,255,255))

        if show_popularity(popularity) == '1':
            new.paste(star,(20, 270), mask=star)
            new.paste(empty_star,(120, 270), mask=empty_star)
            new.paste(empty_star,(220, 270), mask=empty_star)
            new.paste(empty_star,(320, 270), mask=empty_star)
            new.paste(empty_star,(420, 270), mask=empty_star)
        elif show_popularity(popularity) == '2':
            new.paste(star,(20, 270), mask=star)
            new.paste(star,(120, 270), mask=star)
            new.paste(empty_star,(220, 270), mask=empty_star)
            new.paste(empty_star,(320, 270), mask=empty_star)
            new.paste(empty_star,(420, 270), mask=empty_star)
        elif show_popularity(popularity) == '3':
            new.paste(star,(20, 270), mask=star)
            new.paste(star,(120, 270), mask=star)
            new.paste(star,(220, 270), mask=star)
            new.paste(empty_star,(320, 270), mask=empty_star)
            new.paste(empty_star,(420, 270), mask=empty_star)
        elif show_popularity(popularity) == '4':
            new.paste(star,(20, 270), mask=star)
            new.paste(star,(120, 270), mask=star)
            new.paste(star,(220, 270), mask=star)
            new.paste(star,(320, 270), mask=star)
            new.paste(empty_star,(420, 270), mask=empty_star)
        elif show_popularity(popularity) == '5':
            new.paste(star,(20, 270), mask=star)
            new.paste(star,(120, 270), mask=star)
            new.paste(star,(220, 270), mask=star)
            new.paste(star,(320, 270), mask=star)
            new.paste(star,(420, 270), mask=star)
    
        ''' for key, value in tracks_dict.items():
            draw.text((300, 420 + row_space1), str(key) + ".", font=h3_font, fill=(255,255,255))
            draw.text((330, 418 + row_space1), value, font=track_font, fill=(255,255,255))
            row_space1 += 70
        
        for key, value in track_artist_dict.items():
            for i in value:
                draw.text((330, 440 + row_space2), str(value), font=feature_font, fill=(255,255,255))
            row_space2 += 70 '''

        
        for key, value in tracks_dict.items():
            if key < 8 :
                draw.text((30, 420 + row_space1), str(key) + ".", font=h3_font, fill=(255,255,255))
                if len(value) < 30:
                    draw.text((60, 418 + row_space1), value, font=track_font, fill=(255,255,255))
                else: 
                    draw.text((60, 418 + row_space1), value[0:26] + "...", font=track_font, fill=(255,255,255))
            elif key > 7 and key < 15 and total_tracks < 15:
                draw.text((430, 420 + row_space3), str(key) + ".", font=h3_font, fill=(255,255,255))
                draw.text((460, 418 + row_space3), value, font=track_font, fill=(255,255,255))
                row_space3 += 70
            elif key > 7 and key < 15 and total_tracks > 14:
                if key == 14: 
                    draw.text((430, 420 + row_space3), " + " + str(total_tracks - 14) + " more tracks...", font=track_font, fill=(255,255,255))
                else:
                    draw.text((430, 420 + row_space3), str(key) + ".", font=h3_font, fill=(255,255,255))
                    draw.text((460, 418 + row_space3), value, font=track_font, fill=(255,255,255))
                row_space3 += 70
            row_space1 += 70
        
        for key, value in track_artist_dict.items():
            
            if key < 8 :
                feature_space = 60
                for i in value:
                    draw.text((feature_space, 450 + row_space2), str(i), font=feature_font, fill=(255,255,255))
                    #print(i + "=" + str(feature_space) )
                    #feature_space += int(len(str(i)) + 110)
                    feature_space += int(len(str(i)) + 7*int(len(str(i))) + 10)
                    
                row_space2 += 70
            
            elif key > 7 and key < 15 and total_tracks < 15:
                feature_space = 460
                for i in value:
                    draw.text((feature_space, 450 + row_space4), str(i), font=feature_font, fill=(255,255,255))
                    print(i + "=" + str(feature_space) )
                    feature_space += int(len(str(i)) + 7*int(len(str(i))) + 10)
                    
                row_space4 += 70
            
            elif key > 7 and key < 15 and total_tracks > 14:
                feature_space = 460
                for i in value:
                    if key < 14:
                        draw.text((feature_space, 450 + row_space4), str(i), font=feature_font, fill=(255,255,255))
                        print(i + "=" + str(feature_space) )
                        feature_space += int(len(str(i)) + 7*int(len(str(i))) + 10)
                    else: 
                        draw.text((500, 450 + row_space4), "", font=feature_font, fill=(255,255,255))
                    
                row_space4 += 70
        
        
        



        
    
    else:

        draw.text((550, 360), artist_name, font=h3_font, fill=(0,0,0))
        draw.text((20, 30), album_name, font=title_font, fill=(0,0,0))
        draw.text((20, 100), label, font=h3_font, fill=(0,0,0))
        draw.text((20, 140), str(project_type).capitalize(), font=h3_font, fill=(0,0,0))
        draw.text((100, 145), "°", font=h3_font, fill=(0,0,0))
        draw.text((120, 140), release_date, font=h3_font, fill=(0,0,0))
        if total_tracks > 1:
            
            draw.text((20, 180), str(total_tracks) + " tracks", font=h3_font, fill=(0,0,0))
            draw.text((120, 185), "°", font=h3_font, fill=(0,0,0))
            #draw.text((150, 185), duration, font=h3_font, fill=(0,0,0))
        else: 
            draw.text((20, 180), str(total_tracks) + " track", font=h3_font, fill=(0,0,0))
            draw.text((100, 185), "°", font=h3_font, fill=(0,0,0))
            #draw.text((150, 185), duration, font=h3_font, fill=(0,0,0))

        draw.text((100, 210), "Popularity Rating:", font=h2_font, fill=(0,0,0))

        if show_popularity(popularity) == '1':
            new.paste(star,(20, 270), mask=star)
            new.paste(empty_star,(120, 270), mask=empty_star)
            new.paste(empty_star,(220, 270), mask=empty_star)
            new.paste(empty_star,(320, 270), mask=empty_star)
            new.paste(empty_star,(420, 270), mask=empty_star)
        elif show_popularity(popularity) == '2':
            new.paste(star,(20, 270), mask=star)
            new.paste(star,(120, 270), mask=star)
            new.paste(empty_star,(220, 270), mask=empty_star)
            new.paste(empty_star,(320, 270), mask=empty_star)
            new.paste(empty_star,(420, 270), mask=empty_star)
        elif show_popularity(popularity) == '3':
            new.paste(star,(20, 270), mask=star)
            new.paste(star,(120, 270), mask=star)
            new.paste(star,(220, 270), mask=star)
            new.paste(empty_star,(320, 270), mask=empty_star)
            new.paste(empty_star,(420, 270), mask=empty_star)
        elif show_popularity(popularity) == '4':
            new.paste(star,(20, 270), mask=star)
            new.paste(star,(120, 270), mask=star)
            new.paste(star,(220, 270), mask=star)
            new.paste(star,(320, 270), mask=star)
            new.paste(empty_star,(420, 270), mask=empty_star)
        elif show_popularity(popularity) == '5':
            new.paste(star,(20, 270), mask=star)
            new.paste(star,(120, 270), mask=star)
            new.paste(star,(220, 270), mask=star)
            new.paste(star,(320, 270), mask=star)
            new.paste(star,(420, 270), mask=star)
        

        
        ''' for key, value in tracks_dict.items():
            draw.text((300, 420 + row_space1), str(key) + ".", font=h3_font, fill=(0,0,0))
            draw.text((330, 418 + row_space1), value, font=track_font, fill=(0,0,0))
            row_space1 += 70
        
        for key, value in track_artist_dict.items():
            feature_space = 0
            for i in value:
                draw.text((330 + feature_space, 450 + row_space2), str(i), font=feature_font, fill=(0,0,0))
                feature_space += len(str(i)) + 50
            row_space2 += 70 '''
        
        for key, value in tracks_dict.items():
            if key < 8 :
                draw.text((30, 420 + row_space1), str(key) + ".", font=h3_font, fill=(0,0,0))
                if len(value) < 30:
                    draw.text((60, 418 + row_space1), value, font=track_font, fill=(0,0,0))
                else: 
                    draw.text((60, 418 + row_space1), value[0:26] + "...", font=track_font, fill=(0,0,0))
                #print(value + " = " + str(len(value)))
            elif key > 7 and key < 15 and total_tracks < 15:
                draw.text((430, 420 + row_space3), str(key) + ".", font=h3_font, fill=(0,0,0))
                draw.text((460, 418 + row_space3), value, font=track_font, fill=(0,0,0))
                row_space3 += 70
            elif key > 7 and key < 15 and total_tracks > 14:
                if key == 14: 
                    draw.text((430, 420 + row_space3), " + " + str(total_tracks - 14) + " more tracks...", font=track_font, fill=(0,0,0))
                else:
                    draw.text((430, 420 + row_space3), str(key) + ".", font=h3_font, fill=(0,0,0))
                    draw.text((460, 418 + row_space3), value, font=track_font, fill=(0,0,0))
                row_space3 += 70
            row_space1 += 70
        
        for key, value in track_artist_dict.items():
            
            if key < 8 :
                feature_space = 60
                for i in value:
                    draw.text((feature_space, 450 + row_space2), str(i), font=feature_font, fill=(0,0,0))
                    #print(i + "=" + str(feature_space) )
                    #feature_space += int(len(str(i)) + 110)
                    feature_space += int(len(str(i)) + 7*int(len(str(i))) + 10)
                    
                row_space2 += 70
            
            elif key > 7 and key < 15 and total_tracks < 15:
                feature_space = 460
                for i in value:
                    draw.text((feature_space, 450 + row_space4), str(i), font=feature_font, fill=(0,0,0))
                    print(i + " = " + str(feature_space) )
                    feature_space += int(len(str(i)) + 7*int(len(str(i))) + 10)
                    
                row_space4 += 70
            
            elif key > 7 and key < 15 and total_tracks > 14:
                feature_space = 460
                for i in value:
                    if key < 14:
                        draw.text((feature_space, 450 + row_space4), str(i), font=feature_font, fill=(0,0,0))
                        print(i + "=" + str(feature_space) )
                        feature_space += int(len(str(i)) + 7*int(len(str(i))) + 10)
                    else: 
                        draw.text((500, 450 + row_space4), "", font=feature_font, fill=(0,0,0))
                    
                row_space4 += 70
        

        


    new.show()



def show_popularity(popularity):
    print()
    print("  POPULARITY RATING: ", popularity)
    print()
    if popularity < 16:
        print("*")
        return '1'
    elif popularity > 15 and popularity < 32:
        print("* *")
        return '2'
    elif popularity > 31 and popularity < 48:
        print("* * *")
        return '3'
    elif popularity > 47 and popularity < 64:
        print("* * * *")
        return '4'
    elif popularity > 64:
        print("* * * * *")
        return '5'
    

        


def main():
    fetch_spotify_info()
    #isLightOrDark()
    
    

if __name__ == '__main__':
    main()
