from yt_dlp import YoutubeDL


def search_song(song_name):
    ydl_opts = {
        "quiet": True,
        "extract_flat": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(
            f"ytsearch5:{song_name}",
            download=False
        )

        if result["entries"]:
            return result["entries"]

    return []


def download_video(url, save_path, mode, progress_callback=None):

    if mode == "audio":
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": f"{save_path}/%(title)s.%(ext)s",
            "noplaylist": True,

            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        }

    else:
        ydl_opts = {
            "format": "bestvideo+bestaudio/best",
            "outtmpl": f"{save_path}/%(title)s.%(ext)s",
            "merge_output_format": "mp4",
            "noplaylist": True,
        }

    if progress_callback:
        ydl_opts["progress_hooks"] = [progress_callback]

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])