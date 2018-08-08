# coding=utf8

# importing
import requests
import pymongo

# 引入数据库对象，并创建数据库和文档
client = pymongo.MongoClient()
db = client.netease_music
collection = db.playlist
col_music = db.music

# 网易云音乐特定请求头
headers = {
    'Cookie': 'appver=1.5.0.75771',
    'Referer': 'http://music.163.com/',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Mobile Safari/537.36'
}


# 获取歌单并写入数据库
def get_playlist(playlist_id):
    playlist_url = 'http://music.163.com/api/playlist/detail?updateTime=-1&id=' + str(playlist_id)
    playlist_req = requests.get(playlist_url, headers=headers)
    playlist_data = playlist_req.json()
    collection.update_one({'result.id': playlist_data['result']['id']}, {'$set': playlist_data}, upsert=True)


# 获取歌词并写入数据库
def get_lyric(music_id):
    music_url = 'http://music.163.com/api/song/lyric?os=pc&lv=-1&kv=-1&tv=-1&id=' + str(music_id)
    try:
        music_req = requests.get(music_url, headers=headers)
        music_data = music_req.json()
        # 创建字典对象用于存储歌词json
        lrc = {}
        lrc['lyric'] = music_data['lrc']['lyric']
        col_music.update_one({'lyric': lrc['lyric']}, {'$set': lrc}, upsert=True)
    except:
        print 'fail to get ' + str(music_id)
        return


# 歌单爬取主函数
def main(keywords):
    url = 'http://music.163.com/api/search/pc'
    json = {
        's': keywords,
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
    search_words = raw_input('请输入要搜索的关键词： ')
    main(search_words)
    music_playlists = collection.find()
    for music_playlist in music_playlists:
        musics = music_playlist['result']['tracks']
        for music in musics:
            get_lyric(music['id'])
