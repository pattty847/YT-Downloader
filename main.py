import dearpygui.dearpygui as dpg
import dearpygui.demo as demo

from callbacks import CallbackHandler
from pytube import YouTube
from pytube import Playlist
from screeninfo import get_monitors

handler = CallbackHandler()


def on_progress(stream, chunk, bytes_remaining, tag):
    """ Updates download progress to download_placeholder

    Args:
        stream (YouTube Stream): YouTube Object for URL
        chunk (): NA
        bytes_remaining (int): Bytes remaining in download
        tag (_type_): Tag for the text that displays the status
    """
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    pct_completed = bytes_downloaded / total_size * 100
    dpg.set_value(f"{tag}_status_text", f"Status: {round(pct_completed, 2)} %")


def monitors():
    monitors = [s for s in get_monitors()]
    for monitor in monitors:
        if monitor.is_primary:
            return monitor


def start_program():

    dpg.create_context()

    with dpg.window(label="Julian", tag="Primary Window"):
        with dpg.viewport_menu_bar():

            with dpg.menu(label="Settings"):
                download_type = dpg.add_radio_button(
                    ("Audio Only", "Video/Audio"), default_value="Audio Only", horizontal=True, callback=handler.download_type_clicked)

                convert_to_mp3 = dpg.add_checkbox(
                    label="Convert to MP3?", tag="convert-to-audio", default_value=True, callback=handler.convert_audio_to_mp3_clicked)

                with dpg.tooltip(dpg.last_item()):
                    dpg.add_text(
                        "This will convert an audio MP4 file into MP3 (audio only must be selected).")

            dpg.add_menu_item(label="Demo", callback=lambda: demo.show_demo())

        with dpg.child_window(pos=(0, 25)):

            URL = dpg.add_input_text(label="YouTube Playlist URL", width=425, callback=handler.url)

            dpg.add_button(label="Download", callback=handler.download_clicked,
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