import dearpygui.dearpygui as dpg
import dearpygui.demo as demo
import os
from pytube import YouTube
import requests
import re

from screeninfo import get_monitors


def link_snatcher(url):

    # Attempt to make a HTTP GET request to the URL
    our_links = []
    try:
        res = requests.get(url)
    except:
        print('no internet')
        return False

    # Grab the plain text if we get a response
    plain_text = res.text

    # We will now check to see if the URL contains 'list=', which tells us it's a playlist URL from YouTube.
    if 'list=' in url:

        # We will grab the playlist ID by indexing everything after the '='
        # rfind - finds the index of the last occurance of the passed variable
        playlist_index = url.rfind('=') + 1

        # Full playlist URL will be created by indexing from 'eq' to the end of the string
        # Output: PLh325Afkh1nNUktTkPB_f_3YtMdOOITYl
        playlist_ID = url[playlist_index:]
    else:
        print('Incorrect Playlist.')
        return False

    # We now search for this string + playlist ID
    tmp_mat = re.compile(r'watch\?v=\S+?list=' + playlist_ID)
    mat = re.findall(tmp_mat, plain_text)

    # mat - contains list of URLs
    for m in mat:
        new_m = m.replace('&amp;', '&')
        work_m = 'https://youtube.com/' + new_m
        
        # Add the full URL of the video to 'our_links'
        if work_m not in our_links:
            our_links.append(work_m)

    return our_links


def on_progress(stream, chunk, bytes_remaining):
    """Callback function"""
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    pct_completed = bytes_downloaded / total_size * 100
    print(f"Status: {round(pct_completed, 2)} %")


def on_complete():
    pass


def save_videos(new_folder_name, our_links, download_type):

    # Create the folder the downloads will go in
    try:
        os.mkdir(new_folder_name)
    except:
        print('Folder exists.')

    os.chdir(new_folder_name)
    SAVEPATH = "Audio Files"
    dpg.add_text(f'Files will be saved to: {new_folder_name}', parent="downloading")

    dpg.add_text('Connecting to YouTube API...', parent="downloading")


    for link in our_links:
        try:
            yt = YouTube(link, on_progress_callback=on_progress)
            main_title = yt.title
            main_title = main_title.replace('|', '')
            
        except:
            dpg.add_text('Connection issue.', parent="downloading")
            break

        
        try:
            if download_type == "Audio Only":
                vid = yt.streams.filter(only_audio=True).first()
            elif download_type == "Video Only":
                vid = yt.streams.filter(only_video=True).first()
            elif download_type == "Both":
                vid = yt.streams.filter(only_audio=True).first()

                
            dpg.add_text('Downloading - ' + vid.default_filename + ' - File Size -> ' + str(round(vid.filesize / (1024 * 1024), 2)) + ' MB.', parent="downloading")
            vid.download(SAVEPATH)
            dpg.add_text('Complete', parent="downloading")

        except Exception as e:
            print(e)
            dpg.add_text(f'Skipping "{main_title}" error occurred.', parent="downloading")

    
    dpg.add_text('Finished.', parent="downloading")
    dpg.add_text(f'They can be found at: downloads/{SAVEPATH}', parent="downloading")


def monitors():
    monitors = [s for s in get_monitors()]
    for monitor in monitors:
        if monitor.is_primary:
            return monitor


# This function will download the YouTube videos within the Playlist URL
def download(sender, app_data, user_data):
    URL = dpg.get_value(user_data[0])
    DOWNLOAD_TYPE = dpg.get_value(user_data[1])

    if str(URL).startswith("https://www.youtube.com"):
        links = link_snatcher(URL)
        save_videos("downloads", links, DOWNLOAD_TYPE)
    else:
        dpg.add_text("Link must begin with 'https://www.youtube.com'.", parent="downloading")


def download_type_label(sender, app_data, user_data):
    dpg.set_value("download-type-label", "Download Type: " + app_data)


def start_program():
    
    dpg.create_context()

    with dpg.window(label="Julian", tag="Primary Window"):
        with dpg.viewport_menu_bar():
            with dpg.menu(label="Settings"):
                with dpg.menu(label="Download Type"):
                    download_type = dpg.add_radio_button(("Audio Only", "Video Only", "Both"), default_value="Audio Only" , horizontal=True, callback=download_type_label)

            dpg.add_menu_item(label="Demo", callback=lambda: demo.show_demo())

        with dpg.child_window(pos=(0, 25)):

            dpg.add_text("Download Type: " + dpg.get_value(download_type), tag="download-type-label")

            URL = dpg.add_input_text(label="YouTube Playlist URL", width=425)

            dpg.add_button(label="Download", callback = download, user_data=(URL, download_type))

            with dpg.child_window(tag="downloading"):
                pass


    # Primary Window: x and y pos
    x, y = monitors().x, monitors().y

    dpg.create_viewport(title='YouTube Playlist Downloader', x_pos=x, y_pos=y, width=600, height=200, resizable=False)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("Primary Window", True)
    dpg.start_dearpygui()
    dpg.destroy_context()


start_program()