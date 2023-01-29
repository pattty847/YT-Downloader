import dearpygui.dearpygui as dpg
import dearpygui.demo as demo

from pytube import YouTube
from pytube import Playlist
from screeninfo import get_monitors

# TODO: Work on download placeholder - make all videos in playlist show up as placeholders, download thumbnails + add to placeholders, start downloads one by one update progress indicator.


class CallbackHandler():
    def __init__(self) -> None:
        self.download_type = "Audio Only"
        self.convert_to_mp3 = True
        self.url_endpoint = ""

    def url(self, sender, app_data, user_data):
        self.url_endpoint = app_data
        print(self.url_endpoint)

    def downloading_placeholder(
        self, tag: str, identifier: str, message: str
    ) -> None:
        """Creates the default placeholder item for a work."""

        with dpg.child_window(
            tag=f"{tag}_window", parent="console", autosize_x=True, height=50
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

    def download_clicked(self, sender, app_data, user_data):
        if not self.url_endpoint:
            dpg.add_text("Please enter a YouTube Playlist URL.", parent="console")
            return


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

                    audio = youtube.streams.get_audio_only()

                    self.downloading_placeholder(
                        youtube.video_id, audio.title, audio.abr)

                    audio.download(download_path, title +
                                ".mp3" if convert_to_mp3 else ".mp4")

                elif download_type == "Video/Audio":

                    video = youtube.streams.get_highest_resolution()

                    self.downloading_placeholder(
                        youtube.video_id, video.title, video.abr)

                    video.download(download_path, title)

                dpg.delete_item(f"{youtube.video_id}_loading")


    # TODO: Remove print() functions
    def download_type_clicked(self, sender, app_data, user_data):
        self.download_type = app_data
        if app_data == "Video/Audio":
            dpg.set_value("convert-to-audio", False)
        print(app_data)

    def convert_audio_to_mp3_clicked(self, sender, app_data, user_data):
        self.convert_to_mp3 = app_data
        print(app_data)
