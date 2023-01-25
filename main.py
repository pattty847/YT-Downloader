import dearpygui.dearpygui as dpg
import dearpygui.demo as demo
import testing as t

from pytube import YouTube
from pytube import Playlist
from screeninfo import get_monitors


def on_progress(stream, chunk, bytes_remaining, tag):
    """Callback function"""
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    pct_completed = bytes_downloaded / total_size * 100
    dpg.set_value(f"{tag}_status_text", f"Status: {round(pct_completed, 2)} %")


def downloading_placeholder(
    tag: str, identifier: str, message: str
) -> None:
    """Creates the default placeholder item for a work.
        """

    with dpg.child_window(
        tag=f"{tag}_window", parent="console", autosize_x=True, height=35
    ):
        with dpg.group(tag=f"{tag}_group", horizontal=True):
            dpg.add_loading_indicator(tag=f"{tag}_loading", show=True)
            dpg.add_spacer()
            with dpg.group(tag=f"{tag}_content_group", horizontal=True):
                with dpg.child_window(
                    tag=f"{tag}_layout_left",
                    border=False,
                    autosize_x=True,
                    autosize_y=True,
                ):
                    with dpg.group(tag=f"{tag}_heading_group", horizontal=True):
                        dpg.add_text(identifier, tag=f"{tag}_id")
                        with dpg.group(
                            tag=f"{tag}_title_group", horizontal=True,
                        ):
                            dpg.add_text(message, tag=f"{tag}_status_text")


def download(sender, app_data, user_data):

    dpg.add_text("Connecting to YouTube API", parent="console")

    URL, download_type, convert_to_mp3, download_path = dpg.get_value(
        user_data[0]), dpg.get_value(user_data[1]), dpg.get_value(user_data[2]), "Downloads"

    if "playlist" in URL:
        playlist = Playlist(URL)

    for video in playlist.video_urls:
        youtube = YouTube(video)

        title = youtube.title
        thumbnail = youtube.thumbnail_url

        if download_type == "Audio Only":

            downloading_placeholder(youtube.video_id, audio.title, audio.abr)

            audio = youtube.streams.get_audio_only()

            audio.download(download_path, title +
                           ".mp3" if convert_to_mp3 else "")
        elif download_type == "Video/Audio":

            downloading_placeholder(youtube.video_id, audio.title, audio.abr)

            video = youtube.streams.get_highest_resolution()

            video.download(download_path, title)

        dpg.delete_item(f"{youtube.video_id}_loading")


def monitors():
    monitors = [s for s in get_monitors()]
    for monitor in monitors:
        if monitor.is_primary:
            return monitor


def download_type_label(sender, app_data, user_data):
    dpg.set_value("download-type-label", "Download Type: " + app_data)


def start_program():

    dpg.create_context()

    with dpg.window(label="Julian", tag="Primary Window"):
        with dpg.viewport_menu_bar():

            with dpg.menu(label="Settings"):
                download_type = dpg.add_radio_button(
                    ("Audio Only", "Video/Audio"), default_value="Audio Only", horizontal=True, callback=download_type_label)

                convert_to_mp3 = dpg.add_checkbox(
                    label="Convert to MP3?", default_value=True)
                with dpg.tooltip(dpg.last_item()):
                    dpg.add_text(
                        "This will convert an audio MP4 file into MP3.")

            dpg.add_menu_item(label="Demo", callback=lambda: demo.show_demo())

        with dpg.child_window(pos=(0, 25)):

            dpg.add_text("Download Type: " +
                         dpg.get_value(download_type), tag="download-type-label")

            URL = dpg.add_input_text(label="YouTube Playlist URL", width=425)

            dpg.add_button(label="Download", callback=download,
                           user_data=(URL, download_type, convert_to_mp3))

            with dpg.child_window(tag="console"):
                pass

    # Primary Window: x and y pos
    x, y, width, height = monitors().x, monitors().y, monitors().width, monitors().height
    # Centered viewport pos
    x = x + int(width/2-600)
    y = y + int(height/2-500)

    dpg.create_viewport(title='YouTube Playlist Downloader',
                        x_pos=x, y_pos=y, width=600, height=500, resizable=False)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("Primary Window", True)
    dpg.start_dearpygui()
    dpg.destroy_context()


start_program()