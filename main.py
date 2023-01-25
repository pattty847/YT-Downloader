import dearpygui.dearpygui as dpg
import dearpygui.demo as demo
import os
from pytube import YouTube
from pytube import Playlist
import requests
import re
import testing as t

from screeninfo import get_monitors

def on_progress(stream, chunk, bytes_remaining):
    """Callback function"""
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    pct_completed = bytes_downloaded / total_size * 100
    print(f"Status: {round(pct_completed, 2)} %")


def download(sender, app_data, user_data):

    URL, dl_type, convert_to_mp3, download_path = dpg.get_value(user_data[0]), dpg.get_value(user_data[1]), dpg.get_value(user_data[2]), "Downloads"

    playlist = Playlist(URL)

    for video in playlist.video_urls:
        youtube = YouTube(video, on_progress_callback=on_progress)

        title = youtube.title
        thumbnail = youtube.thumbnail_url

        if dl_type == "Audio Only":
            audio = youtube.streams.get_audio_only()

            print(f"Downloading: {title} | APR: {audio.abr}")
            audio.download(download_path, title + ".mp3" if convert_to_mp3 else "")
        elif dl_type == "Video/Audio":
            video = youtube.streams.get_highest_resolution()

            print(f"Downloading: {title} | FPS: {video.fps} | RES: {video.resolution}")
            video.download(download_path, title)

        # Push download to console
        


# def save_videos(saved_path, our_links, download_type, convert):

#     # Create the folder the downloads will go in
#     try:
#         os.mkdir(saved_path)
#     except:
#         print('Folder exists.')

#     dpg.add_text(f'Files will be saved to: {saved_path}', parent="downloading")

#     dpg.add_text('Connecting to YouTube API...', parent="downloading", color=(242, 21, 72, 255))

#     if convert:
#         dpg.add_text('Converting MP4 to MP3.', parent="downloading")

#     x=[]
#     for root, dirs, files in os.walk(".", topdown=False):
#         for name in files:
#             pathh = os.path.join(root, name)

            
#             if os.path.getsize(pathh) < 1:
#                 os.remove(pathh)
#             else:
#                 x.append(str(name))


#     for link in our_links:
#         try:
#             yt = YouTube(link, on_progress_callback=on_progress)
#             main_title = yt.title
#             main_title = main_title.replace('|', '')

            
#         except:
#             dpg.add_text('Connection issue.', parent="downloading")
#             break

        
#         # Check if we have already downloaded this file before
#         if main_title not in x:

#             dpg.add_text(f"Beginning: " + main_title, parent="downloading", color=(163, 186, 30, 255))

            
#             if download_type == "Audio Only":
#                 vid = yt.streams.get_audio_only()
#                 vid.download(saved_path, filename=main_title+'.mp3' if convert else '.mp4')

#             elif download_type == "Video Only":
#                 vid = yt.streams.filter(only_video=True)
#                 vid.download(saved_path, filename=main_title+'.mp3' if convert else '.mp4')
#             elif download_type == "Both":
#                 vid = yt.streams.filter(progressive=True)
#                 vid.download(saved_path, filename=main_title+'.mp3' if convert else '.mp4')


#             dpg.add_text(f"Finished: " + main_title, parent="downloading", color=(30, 186, 43, 255))


#         else:
#             dpg.add_text(f'Skipping "{main_title}" already downloaded.', parent="downloading")

    
#     dpg.add_text('Finished.', parent="downloading", color=(21, 39, 242, 0.8))
#     dpg.add_text(f'They can be found at: {saved_path}', parent="downloading")


def monitors():
    monitors = [s for s in get_monitors()]
    for monitor in monitors:
        if monitor.is_primary:
            return monitor


def download_type_label(sender, app_data, user_data):
    dpg.set_value("download-type-label", "Download Type: " + app_data)


def convert_type_label(sender, app_data, user_data):
    dpg.set_value("convert-type-label", app_data)


def start_program():
    
    dpg.create_context()

    with dpg.window(label="Julian", tag="Primary Window"):
        with dpg.viewport_menu_bar():

            with dpg.menu(label="Settings"):
                download_type = dpg.add_radio_button(("Audio Only", "Video/Audio"), default_value="Audio Only" , horizontal=True, callback=download_type_label)
                
                conversion_type = dpg.add_checkbox(label="Convert to MP3?", default_value=True)

            dpg.add_menu_item(label="Demo", callback=lambda: demo.show_demo())

        with dpg.child_window(pos=(0, 25)):

            dpg.add_text("Download Type: " + dpg.get_value(download_type), tag="download-type-label")

            URL = dpg.add_input_text(label="YouTube Playlist URL", width=425)

            dpg.add_button(label="Download", callback = download, user_data=(URL, download_type, conversion_type))

            with dpg.child_window(tag="downloading"):
                pass

    # Primary Window: x and y pos
    x, y, width, height = monitors().x, monitors().y, monitors().width, monitors().height
    # Centered viewport pos
    x = x + int(width/2-600)
    y = y + int(height/2-500)

    dpg.create_viewport(title='YouTube Playlist Downloader', x_pos=x, y_pos=y, width=600, height=500, resizable=False)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("Primary Window", True)
    dpg.start_dearpygui()
    dpg.destroy_context()


start_program()