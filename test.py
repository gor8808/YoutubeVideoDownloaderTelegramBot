from pytube import YouTube
import os
from moviepy.editor import *
import telebot
import config
import re
import uuid
from telebot import types
regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
bot = telebot.TeleBot(config.TOKEN)
print("Start working")
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	markup = types.ReplyKeyboardMarkup(row_width=2)
	itembtn1 = types.KeyboardButton('video')
	itembtn2 = types.KeyboardButton('mp3')
	itembtn3 = types.KeyboardButton('mp3 from local video')
	markup.add(itembtn1, itembtn2, itembtn3)
	bot.send_message(message.chat.id, "Choose one letter:", reply_markup=markup)

downloadType = "none"
@bot.message_handler(content_types=['text'])
def lalala(message):
	global downloadType
	markup = types.ReplyKeyboardMarkup(row_width=2)
	itembtn1 = types.KeyboardButton('video')
	itembtn2 = types.KeyboardButton('mp3')
	itembtn3 = types.KeyboardButton('mp3 from local video')
	markup.add(itembtn1, itembtn2, itembtn3)
	bot.send_message(message.chat.id, "Choose downloading type:", reply_markup=markup)
	if message.text[0] == '/':
		pass
	if message.text == "video":
			# bot.send_message(message.chat.id,"You choose video type \nPlease send me the video link from youtube and" +
			# " i will send you downloaded video")
		downloadType = "video"
	elif message.text == "mp3":
		bot.send_message(message.chat.id,"You choose mp3 type")
		downloadType = "mp3"
	elif message.text == "mp3 from local video":
		bot.send_message(message.chat.id,"You choose mp3 from local video type")
		downloadType = "mp3 from local video"
	elif re.match(regex, message.text) is not None:
		if(downloadType == "video"):
			url = message.text
			Video = YouTube(url)
			print("Your url --- " + url)
			path = "C:\\Users\\Dell\\Desktop\\Gor\\Python\\YoutubeVideoDownload\\"
			print("Downloading in progress please wait!!")
			bot.send_message(message.chat.id,"Downloading in progress please wait!!")
			VideoUUID = str(uuid.uuid4())
			Video.streams.first().download(path+"Videos",filename='video' + VideoUUID)
			video = open(path + "Videos\\" + "video" + VideoUUID + ".mp4","rb")
			print("Open ")
			bot.send_document(message.chat.id,video)
			bot.send_message(message.chat.id,"Successfully sent	!!")
		# elif downloadType == "mp3":

		# url = message.text
        # Video = YouTube(url)
        # print("Your url --- " + url)
        # path = "C:\\Users\\Dell\\Desktop\\Gor\\Python\\YoutubeVideoDownload\\"
        # print("Downloading in progress please wait!!")
        # bot.send_message(message.chat.id,"Downloading in progress please wait!!")
        # VideoUUID = str(uuid.uuid4())
        # Video.streams.first().download(path+"Videos",filename='video' + VideoUUID)
        # video = VideoFileClip(os.path.join(path+"Videos\\" + 'video' + VideoUUID + ".mp4"))
        # video.audio.write_audiofile(os.path.join(path + "MP3\\" + Video.title.replace('/'," ").replace("\\"," ") + ".mp3"))
        # bot.send_message(message.chat.id,"Video Thumbnail")
        # bot.send_photo(message.chat.id,Video.thumbnail_url)
        # audio = open(path + "MP3\\" + Video.title.replace('/'," ") + ".mp3","rb")
        # bot.send_audio(message.chat.id,audio,title = Video.title,duration = Video.length)
        # print("Successfully downloaded!!")
        # bot.send_message(message.chat.id,"Successfully sent!!")
	else:
		bot.send_message(message.chat.id,"Not walid url")
		pass
	# else:
	# 	bot.send_message(message.chat.id,"Download type -- " + downloadType)
		
bot.polling()