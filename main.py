import dearpygui.dearpygui as dpg
import dearpygui.demo as demo
import testing as t

from pytube import YouTube
from pytube import Playlist
from screeninfo import get_monitors

def on_progress(stream, chunk, bytes_remaining):
    """Callback function"""
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    pct_completed = bytes_downloaded / total_size * 100
    print(f"Status: {round(pct_completed, 2)} %")


def download(sender, app_data, user_data):

    URL, download_type, convert_to_mp3, download_path = dpg.get_value(user_data[0]), dpg.get_value(user_data[1]), dpg.get_value(user_data[2]), "Downloads"

    playlist = Playlist(URL)

    for video in playlist.video_urls:
        youtube = YouTube(video, on_progress_callback=on_progress)

        title = youtube.title
        thumbnail = youtube.thumbnail_url

        if download_type == "Audio Only":
            audio = youtube.streams.get_audio_only()

            print(f"Downloading: {title} | APR: {audio.abr}")
            audio.download(download_path, title + ".mp3" if convert_to_mp3 else "")
        elif download_type == "Video/Audio":
            video = youtube.streams.get_highest_resolution()

            print(f"Downloading: {title} | FPS: {video.fps} | RES: {video.resolution}")
            video.download(download_path, title)

        # Push download to console
        


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
                
                convert_to_mp3 = dpg.add_checkbox(label="Convert to MP3?", default_value=True)

            dpg.add_menu_item(label="Demo", callback=lambda: demo.show_demo())

        with dpg.child_window(pos=(0, 25)):

            dpg.add_text("Download Type: " + dpg.get_value(download_type), tag="download-type-label")

            URL = dpg.add_input_text(label="YouTube Playlist URL", width=425)

            dpg.add_button(label="Download", callback = download, user_data=(URL, download_type, convert_to_mp3))

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