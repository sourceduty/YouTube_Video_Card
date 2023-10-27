# YouTube_Video_Card

# 📺 YouTube video information cards.

# Copyright (C) 2023, Sourceduty - All Rights Reserved.
# THE CONTENTS OF THIS PROJECT ARE PROPRIETARY.

import requests
from PIL import Image, ImageDraw, ImageFont
from pytube import YouTube
from pytube.exceptions import VideoUnavailable

FONT_NAME = "arial.ttf"
FONT_SIZE = 20
FONT_COLOR = "white"

def get_youtube_details(video_url):
    try:
        yt = YouTube(video_url)
        vid_info = yt.vid_info
        return {
            'video_title': yt.title,
            'video_description': yt.description,
            'video_thumbnail_url': yt.thumbnail_url,
            'channel_title': yt.author,
            'video_url': video_url,
            'views': yt.views,
            'likes': vid_info.get('likeCount', 'N/A'),
            'dislikes': vid_info.get('dislikeCount', 'N/A')
        }
    except VideoUnavailable:
        print("The provided YouTube video URL is invalid or the video is unavailable.")
        exit()

def download_image(url):
    try:
        return Image.open(requests.get(url, stream=True).raw)
    except requests.RequestException:
        print(f"Failed to download image from {url}")
        exit()

def add_text_to_image(image, details):
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype(FONT_NAME, FONT_SIZE)
    except IOError:
        print(f"Font {FONT_NAME} not found. Using default font.")
        font = ImageFont.load_default()

    y_offset = 10
    draw.text((10, y_offset), details['video_title'], font=font, fill=FONT_COLOR)
    y_offset += 30
    draw.text((10, y_offset), details['channel_title'], font=font, fill=FONT_COLOR)
    y_offset += 30
    draw.text((10, y_offset), f"URL: {details['video_url']}", font=font, fill=FONT_COLOR)
    y_offset += 30
    draw.text((10, y_offset), f"Views: {details['views']}", font=font, fill=FONT_COLOR)
    y_offset += 30
    draw.text((10, y_offset), f"Likes: {details['likes']}", font=font, fill=FONT_COLOR)
    y_offset += 30
    draw.text((10, y_offset), f"Dislikes: {details['dislikes']}", font=font, fill=FONT_COLOR)

if __name__ == "__main__":
    video_url = input("Enter the YouTube video URL: ")
    details = get_youtube_details(video_url)

    video_thumbnail = download_image(details['video_thumbnail_url'])

    add_text_to_image(video_thumbnail, details)

    video_thumbnail.save('compiled_image.jpg')
    print("Image saved as compiled_image.jpg")
