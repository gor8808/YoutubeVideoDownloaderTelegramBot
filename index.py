
from pytube import YouTube
import os
from moviepy.editor import *
import telebot
import config
import re
import uuid

try:
    regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    bot = telebot.TeleBot(config.TOKEN)
    @bot.message_handler(commands=['start', 'help'])
    def send_welcome(message):
        bot.reply_to(message, "Just share with me video link from youtube.")
    @bot.message_handler(content_types=['text'])
    def sendMessage(message):
        if message.text[0] == '/':
            pass
        elif re.match(regex, message.text) is not None:
            url = message.text
            Video = YouTube(url)
            print("Your url --- " + url)
            path = "C:\\Users\\Dell\\Desktop\\Gor\\Python\\TelegramBot\\YoutubeVideoDownload\\"
            print("Downloading in progress please wait!!")
            bot.send_message(message.chat.id,"Downloading in progress please wait!!")
            VideoUUID = str(uuid.uuid4())
            Video.streams.first().download(path+"Videos",filename='video' + VideoUUID)
            video = VideoFileClip(os.path.join(path+"Videos\\" + 'video' + VideoUUID + ".mp4"))
            video.audio.write_audiofile(os.path.join(path + "MP3\\" + Video.title.replace('/'," ").replace("\\"," ") + ".mp3"))
            bot.send_message(message.chat.id,"Video Thumbnail")
            bot.send_photo(message.chat.id,Video.thumbnail_url)
            audio = open(path + "MP3\\" + Video.title.replace('/'," ") + ".mp3","rb")
            bot.send_audio(message.chat.id,audio,title = Video.title,duration = Video.length)
            print("Successfully downloaded!!")
            bot.send_message(message.chat.id,"Successfully sent!!")
        else:
            bot.send_message(message.chat.id,"Not walid url")
            pass
    bot.polling()
except IOError:
    print("IOError")