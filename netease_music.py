# coding=utf8

import requests
import pymongo

client = pymongo.MongoClient()
db = client.netease_music
collection = db.playlist
col_music = db.music

headers = {
    'Cookie': 'appver=1.5.0.75771',
    'Referer': 'http://music.163.com/',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Mobile Safari/537.36'
}


def get_playlist(playlist_id):
    playlist_url = 'http://music.163.com/api/playlist/detail?updateTime=-1&id=' + str(playlist_id)
    playlist_req = requests.get(playlist_url, headers=headers)
    playlist_data = playlist_req.json()
    collection.update_one({'result.id': playlist_data['result']['id']}, {'$set': playlist_data}, upsert=True)


def get_lyric(music_id):
    music_url = 'http://music.163.com/api/song/lyric?os=pc&lv=-1&kv=-1&tv=-1&id=' + str(music_id)
    try:
        music_req = requests.get(music_url, headers=headers)
        music_data = music_req.json()
        lrc = {}
        lrc['lyric'] = music_data['lrc']['lyric']
        col_music.update_one({'lyric': lrc['lyric']}, {'$set': lrc}, upsert=True)
    except:
        print 'fail to get ' + str(music_id)
        return


def main():
    url = 'http://music.163.com/api/search/pc'
    json = {
        's': '程序员',
        'offset': 0,
        'limit': 10,
        'type': 1000
    }
    req = requests.post(url, data=json, headers=headers)
    data = req.json()
    result = data['result']
    for playlist in result['playlists']:
        get_playlist(playlist['id'])


if __name__ == '__main__':
    main()
    music_playlists = collection.find()
    for music_playlist in music_playlists:
        musics = music_playlist['result']['tracks']
        for music in musics:
            get_lyric(music['id'])
