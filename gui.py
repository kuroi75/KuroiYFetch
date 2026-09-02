import tkinter as tk
from tkinter import ttk, filedialog
import threading

from youtube import search_song, download_video


# =========================================================
# GLOBAL VARIABLES
# =========================================================

current_results = []
selected_url = None

current_mode = "individual"
is_downloading = False

SEARCH_PLACEHOLDER = "Search here or paste link..."


# =========================================================
# WINDOW
# =========================================================

window = tk.Tk()

window.title("🎵 KuroiYFetch YouTube Downloader")
window.geometry("950x720")
window.minsize(750, 600)

window.columnconfigure(0, weight=1)
window.rowconfigure(2, weight=1)


# =========================================================
# VARIABLES
# =========================================================

folder_var = tk.StringVar()
download_mode = tk.StringVar(value="Audio (MP3)")


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def is_youtube_url(text):
    text = text.lower()

    return (
        text.startswith("http://")
        or text.startswith("https://")
    ) and (
        "youtube.com" in text
        or "youtu.be" in text
    )


def get_search_text():

    text = search_entry.get().strip()

    if text == SEARCH_PLACEHOLDER:
        return ""

    return text


# =========================================================
# PLACEHOLDER
# =========================================================

def clear_placeholder(event=None):

    if search_entry.get() == SEARCH_PLACEHOLDER:
        search_entry.delete(0, tk.END)
        search_entry.config(fg="black")


def restore_placeholder(event=None):

    if not search_entry.get().strip():
        search_entry.insert(0, SEARCH_PLACEHOLDER)
        search_entry.config(fg="gray")


# =========================================================
# MODE SWITCHING
# =========================================================

def switch_individual_mode():

    global current_mode

    current_mode = "individual"

    individual_button.config(
        relief="sunken"
    )

    bulk_button.config(
        relief="raised"
    )

    status.config(
        text="👤 Individual Download mode"
    )

    search_entry.focus_set()


def switch_bulk_mode():

    global current_mode

    current_mode = "bulk"

    individual_button.config(
        relief="raised"
    )

    bulk_button.config(
        relief="sunken"
    )

    status.config(
        text="📦 Bulk Download mode"
    )

    open_bulk_popup()


# =========================================================
# SEARCH
# =========================================================

def search_from_bar():

    global current_results
    global selected_url

    query = get_search_text()

    if not query:

        status.config(
            text="⚠ Please enter a song/video name or paste a YouTube link."
        )

        return

    if current_mode != "individual":

        open_bulk_popup()
        return

    selected_url = None

    search_button.config(
        state="disabled"
    )

    status.config(
        text="🔎 Searching..."
    )

    # -----------------------------------------------------
    # Clear old results
    # -----------------------------------------------------

    result_list.delete(
        0,
        tk.END
    )

    def worker():

        global current_results
        global selected_url

        try:

            # -------------------------------------------------
            # DIRECT YOUTUBE LINK
            # -------------------------------------------------

            if is_youtube_url(query):

                current_results = []
                selected_url = query

                window.after(
                    0,
                    lambda: direct_link_ready(query)
                )

                return

            # -------------------------------------------------
            # SEARCH BY NAME
            # -------------------------------------------------

            results = search_song(query)

            current_results = results
            selected_url = None

            window.after(
                0,
                lambda r=results: display_results(r)
            )

        except Exception as error:

            window.after(
                0,
                lambda err=str(error): search_error(err)
            )

        finally:

            window.after(
                0,
                lambda: search_button.config(
                    state="normal"
                )
            )

    threading.Thread(
        target=worker,
        daemon=True
    ).start()


# =========================================================
# DIRECT LINK
# =========================================================

def direct_link_ready(url):

    result_list.delete(
        0,
        tk.END
    )

    status.config(
        text="🔗 YouTube link ready!\n"
             "Choose MP3/MP4 and press DOWNLOAD."
    )


# =========================================================
# DISPLAY SEARCH RESULTS
# =========================================================

def display_results(results):

    result_list.delete(
        0,
        tk.END
    )

    if not results:

        status.config(
            text="❌ No results found."
        )

        return

    for video in results:

        title = video.get(
            "title",
            "Unknown title"
        )

        channel = video.get(
            "channel"
        ) or video.get(
            "uploader",
            "Unknown channel"
        )

        duration = video.get(
            "duration"
        )

        if duration:

            minutes = int(duration) // 60
            seconds = int(duration) % 60

            duration_text = (
                f"{minutes}:{seconds:02d}"
            )

        else:

            duration_text = ""

        display_text = title

        if channel:

            display_text += (
                f"  |  {channel}"
            )

        if duration_text:

            display_text += (
                f"  |  {duration_text}"
            )

        result_list.insert(
            tk.END,
            display_text
        )

    status.config(
        text=f"✅ Found {len(results)} results. "
             f"Select one and press SELECT RESULT."
    )


# =========================================================
# SEARCH ERROR
# =========================================================

def search_error(error):

    status.config(
        text=f"❌ Search failed:\n{error}"
    )


# =========================================================
# SELECT RESULT
# =========================================================

def select_result():

    global selected_url

    selected = result_list.curselection()

    if not selected:

        status.config(
            text="⚠ Please select a result first."
        )

        return

    index = selected[0]

    video = current_results[index]

    video_id = video.get("id")

    if not video_id:

        status.config(
            text="❌ Could not get video ID."
        )

        return

    selected_url = (
        f"https://youtube.com/watch?v={video_id}"
    )

    title = video.get(
        "title",
        "Unknown"
    )

    channel = video.get(
        "channel"
    ) or video.get(
        "uploader",
        "Unknown"
    )

    status.config(
        text=f"✅ Selected:\n"
             f"🎵 {title}\n"
             f"👤 {channel}"
    )


# =========================================================
# FOLDER
# =========================================================

def choose_folder():

    folder = filedialog.askdirectory()

    if folder:

        folder_var.set(folder)

        status.config(
            text=f"📁 Save folder selected."
        )


# =========================================================
# DOWNLOAD MODE
# =========================================================

def get_download_mode():

    if download_mode.get() == "Audio (MP3)":

        return "audio"

    return "video"


# =========================================================
# DOWNLOAD PROGRESS
# =========================================================

def update_progress(data):

    try:

        if data["status"] == "downloading":

            percent = data.get(
                "_percent_str",
                "0%"
            )

            speed = data.get(
                "_speed_str",
                "Unknown"
            )

            eta = data.get(
                "_eta_str",
                "?"
            )

            window.after(
                0,
                lambda p=percent, s=speed, e=eta:
                progress_label.config(
                    text=f"⬇ {p} | {s} | ETA: {e}"
                )
            )

        elif data["status"] == "finished":

            window.after(
                0,
                lambda:
                progress_label.config(
                    text="🔄 Processing file..."
                )
            )

    except Exception:
        pass


# =========================================================
# DOWNLOAD CURRENT VIDEO
# =========================================================

def download_current():

    global is_downloading

    if is_downloading:

        return

    if not selected_url:

        status.config(
            text="⚠ Search for a video, select a result, "
                 "or paste a YouTube link first."
        )

        return

    folder = folder_var.get().strip()

    if not folder:

        status.config(
            text="⚠ Please choose a save folder first."
        )

        return

    mode = get_download_mode()

    is_downloading = True

    download_button.config(
        state="disabled"
    )

    individual_button.config(
        state="disabled"
    )

    bulk_button.config(
        state="disabled"
    )

    search_button.config(
        state="disabled"
    )

    progress_label.config(
        text="⏳ Preparing download..."
    )

    status.config(
        text="⬇ Starting download..."
    )

    url = selected_url

    def worker():

        try:

            download_video(
                url,
                folder,
                mode,
                update_progress
            )

            window.after(
                0,
                download_finished
            )

        except Exception as error:

            window.after(
                0,
                lambda err=str(error):
                download_error(err)
            )

    threading.Thread(
        target=worker,
        daemon=True
    ).start()


# =========================================================
# DOWNLOAD FINISHED
# =========================================================

def download_finished():

    global is_downloading

    is_downloading = False

    download_button.config(
        state="normal"
    )

    individual_button.config(
        state="normal"
    )

    bulk_button.config(
        state="normal"
    )

    search_button.config(
        state="normal"
    )

    progress_label.config(
        text="🎉 File saved successfully!"
    )

    status.config(
        text="✅ Download completed!"
    )


# =========================================================
# DOWNLOAD ERROR
# =========================================================

def download_error(error):

    global is_downloading

    is_downloading = False

    download_button.config(
        state="normal"
    )

    individual_button.config(
        state="normal"
    )

    bulk_button.config(
        state="normal"
    )

    search_button.config(
        state="normal"
    )

    status.config(
        text=f"❌ Download failed:\n{error}"
    )


# =========================================================
# LOAD songs.txt
# =========================================================

def load_songs_file():

    try:

        with open(
            "songs.txt",
            "r",
            encoding="utf-8"
        ) as file:

            return [
                line.strip()
                for line in file
                if line.strip()
            ]

    except FileNotFoundError:

        return []


# =========================================================
# BULK DOWNLOAD POPUP
# =========================================================

def open_bulk_popup():

    popup = tk.Toplevel(window)

    popup.title("📦 Bulk Download")
    popup.geometry("650x560")
    popup.minsize(550, 450)

    popup.transient(window)
    popup.grab_set()

    popup.columnconfigure(
        0,
        weight=1
    )

    popup.rowconfigure(
        2,
        weight=1
    )

    # -----------------------------------------------------
    # TITLE
    # -----------------------------------------------------

    tk.Label(
        popup,
        text="📦 Bulk Download",
        font=("Arial", 18, "bold")
    ).grid(
        row=0,
        column=0,
        pady=(18, 5)
    )

    tk.Label(
        popup,
        text=(
            "Put one video/song name or YouTube link per line.\n"
            "You can also use the existing songs.txt file."
        ),
        font=("Arial", 10),
        justify="center"
    ).grid(
        row=1,
        column=0,
        pady=(0, 10)
    )

    # -----------------------------------------------------
    # TEXT BOX
    # -----------------------------------------------------

    text_frame = tk.Frame(popup)

    text_frame.grid(
        row=2,
        column=0,
        sticky="nsew",
        padx=20,
        pady=5
    )

    text_frame.columnconfigure(
        0,
        weight=1
    )

    text_frame.rowconfigure(
        0,
        weight=1
    )

    bulk_text = tk.Text(
        text_frame,
        font=("Consolas", 11),
        wrap="word"
    )

    bulk_text.grid(
        row=0,
        column=0,
        sticky="nsew"
    )

    scrollbar = ttk.Scrollbar(
        text_frame,
        orient="vertical",
        command=bulk_text.yview
    )

    scrollbar.grid(
        row=0,
        column=1,
        sticky="ns"
    )

    bulk_text.config(
        yscrollcommand=scrollbar.set
    )

    # -----------------------------------------------------
    # LOAD songs.txt
    # -----------------------------------------------------

    def use_songs_file():

        songs = load_songs_file()

        bulk_text.delete(
            "1.0",
            tk.END
        )

        if songs:

            bulk_text.insert(
                "1.0",
                "\n".join(songs)
            )

            status.config(
                text=f"📂 Loaded {len(songs)} items from songs.txt"
            )

        else:

            status.config(
                text="⚠ songs.txt is empty or does not exist."
            )

    # -----------------------------------------------------
    # SAVE TO songs.txt
    # -----------------------------------------------------

    def save_songs():

        content = bulk_text.get(
            "1.0",
            tk.END
        ).strip()

        if not content:

            status.config(
                text="⚠ Nothing to save."
            )

            return

        try:

            with open(
                "songs.txt",
                "w",
                encoding="utf-8"
            ) as file:

                file.write(
                    content + "\n"
                )

            status.config(
                text="💾 Saved to songs.txt"
            )

        except Exception as error:

            status.config(
                text=f"❌ Could not save songs.txt: {error}"
            )

    # -----------------------------------------------------
    # START BULK DOWNLOAD
    # -----------------------------------------------------

    def start_from_text():

        content = bulk_text.get(
            "1.0",
            tk.END
        ).strip()

        if not content:

            status.config(
                text="⚠ Please enter at least one item."
            )

            return

        songs = [
            line.strip()
            for line in content.splitlines()
            if line.strip()
        ]

        popup.destroy()

        start_bulk_download(
            songs
        )

    # -----------------------------------------------------
    # START FROM songs.txt
    # -----------------------------------------------------

    def start_from_file():

        songs = load_songs_file()

        if not songs:

            status.config(
                text="⚠ songs.txt is empty or missing."
            )

            return

        popup.destroy()

        start_bulk_download(
            songs
        )

    # -----------------------------------------------------
    # BUTTONS
    # -----------------------------------------------------

    button_frame = tk.Frame(popup)

    button_frame.grid(
        row=3,
        column=0,
        pady=15
    )

    tk.Button(
        button_frame,
        text="📂 USE songs.txt",
        font=("Arial", 10),
        padx=12,
        pady=8,
        command=use_songs_file
    ).pack(
        side="left",
        padx=4
    )

    tk.Button(
        button_frame,
        text="💾 SAVE TO songs.txt",
        font=("Arial", 10),
        padx=12,
        pady=8,
        command=save_songs
    ).pack(
        side="left",
        padx=4
    )

    tk.Button(
        button_frame,
        text="▶ START BULK DOWNLOAD",
        font=("Arial", 10, "bold"),
        padx=12,
        pady=8,
        command=start_from_text
    ).pack(
        side="left",
        padx=4
    )

    tk.Button(
        button_frame,
        text="❌ CANCEL",
        font=("Arial", 10),
        padx=12,
        pady=8,
        command=popup.destroy
    ).pack(
        side="left",
        padx=4
    )


# =========================================================
# START BULK DOWNLOAD
# =========================================================

def start_bulk_download(songs):

    global is_downloading

    if is_downloading:

        return

    folder = folder_var.get().strip()

    if not folder:

        status.config(
            text="⚠ Please choose a save folder first."
        )

        return

    mode = get_download_mode()

    is_downloading = True

    download_button.config(
        state="disabled"
    )

    individual_button.config(
        state="disabled"
    )

    bulk_button.config(
        state="disabled"
    )

    search_button.config(
        state="disabled"
    )

    total = len(songs)

    status.config(
        text=f"📦 Starting bulk download of {total} items..."
    )

    progress_label.config(
        text="⏳ Preparing..."
    )

    def worker():

        for index, item in enumerate(songs):

            try:

                number = index + 1

                # -------------------------------------------------
                # SHOW SEARCH STATUS
                # -------------------------------------------------

                window.after(
                    0,
                    lambda n=number, t=total, s=item:
                    status.config(
                        text=f"🔎 Searching {n}/{t}: {s}"
                    )
                )

                # -------------------------------------------------
                # IF IT IS ALREADY A LINK
                # -------------------------------------------------

                if is_youtube_url(item):

                    url = item

                # -------------------------------------------------
                # OTHERWISE SEARCH THE NAME
                # -------------------------------------------------

                else:

                    results = search_song(item)

                    if not results:

                        window.after(
                            0,
                            lambda s=item:
                            status.config(
                                text=f"❌ No results found for: {s}"
                            )
                        )

                        continue

                    video = results[0]

                    video_id = video.get(
                        "id"
                    )

                    if not video_id:

                        window.after(
                            0,
                            lambda s=item:
                            status.config(
                                text=f"❌ No video ID for: {s}"
                            )
                        )

                        continue

                    url = (
                        f"https://youtube.com/watch?v={video_id}"
                    )

                # -------------------------------------------------
                # DOWNLOAD
                # -------------------------------------------------

                window.after(
                    0,
                    lambda n=number, t=total, s=item:
                    status.config(
                        text=f"⬇ Downloading {n}/{t}: {s}"
                    )
                )

                download_video(
                    url,
                    folder,
                    mode,
                    update_progress
                )

                window.after(
                    0,
                    lambda n=number, t=total, s=item:
                    status.config(
                        text=f"✅ Finished {n}/{t}: {s}"
                    )
                )

            except Exception as error:

                window.after(
                    0,
                    lambda s=item, err=str(error):
                    status.config(
                        text=f"❌ Failed: {s}\n{err}"
                    )
                )

        window.after(
            0,
            bulk_download_finished
        )

    threading.Thread(
        target=worker,
        daemon=True
    ).start()


# =========================================================
# BULK DOWNLOAD FINISHED
# =========================================================

def bulk_download_finished():

    global is_downloading

    is_downloading = False

    download_button.config(
        state="normal"
    )

    individual_button.config(
        state="normal"
    )

    bulk_button.config(
        state="normal"
    )

    search_button.config(
        state="normal"
    )

    progress_label.config(
        text="🎉 Bulk download completed!"
    )

    status.config(
        text="✅ All bulk downloads finished!"
    )


# =========================================================
# TITLE
# =========================================================

title = tk.Label(
    window,
    text="🎵 KuroiYFetch YouTube Downloader",
    font=("Arial", 23, "bold")
)

title.grid(
    row=0,
    column=0,
    pady=(18, 8)
)


# =========================================================
# MODE BUTTONS
# =========================================================

mode_frame = tk.Frame(
    window
)

mode_frame.grid(
    row=1,
    column=0,
    pady=(0, 12)
)


individual_button = tk.Button(
    mode_frame,
    text="👤 INDIVIDUAL DOWNLOAD",
    font=("Arial", 11, "bold"),
    padx=18,
    pady=9,
    relief="sunken",
    cursor="hand2",
    command=switch_individual_mode
)

individual_button.pack(
    side="left",
    padx=5
)


bulk_button = tk.Button(
    mode_frame,
    text="📦 BULK DOWNLOAD",
    font=("Arial", 11, "bold"),
    padx=18,
    pady=9,
    relief="raised",
    cursor="hand2",
    command=switch_bulk_mode
)

bulk_button.pack(
    side="left",
    padx=5
)


# =========================================================
# MAIN CONTENT
# =========================================================

main_frame = tk.Frame(
    window
)

main_frame.grid(
    row=2,
    column=0,
    sticky="nsew",
    padx=25,
    pady=5
)

main_frame.columnconfigure(
    0,
    weight=1
)

main_frame.rowconfigure(
    2,
    weight=1
)


# =========================================================
# SEARCH BAR
# =========================================================

search_frame = tk.Frame(
    main_frame
)

search_frame.grid(
    row=0,
    column=0,
    sticky="ew",
    pady=(0, 12)
)

search_frame.columnconfigure(
    1,
    weight=1
)


# ---------------------------------------------------------
# YOUTUBE LOGO
# ---------------------------------------------------------

youtube_logo = tk.Canvas(
    search_frame,
    width=55,
    height=50,
    highlightthickness=0,
    bg=window.cget("bg")
)

youtube_logo.grid(
    row=0,
    column=0,
    padx=(0, 8)
)

youtube_logo.create_rectangle(
    5,
    7,
    50,
    43,
    fill="#FF0000",
    outline="#FF0000"
)

youtube_logo.create_polygon(
    23,
    15,
    23,
    35,
    38,
    25,
    fill="white",
    outline="white"
)


# ---------------------------------------------------------
# SEARCH ENTRY
# ---------------------------------------------------------

search_entry = tk.Entry(
    search_frame,
    font=("Arial", 15),
    fg="gray",
    relief="solid",
    bd=1
)

search_entry.grid(
    row=0,
    column=1,
    sticky="ew",
    ipady=9
)

search_entry.insert(
    0,
    SEARCH_PLACEHOLDER
)

search_entry.bind(
    "<FocusIn>",
    clear_placeholder
)

search_entry.bind(
    "<FocusOut>",
    restore_placeholder
)

search_entry.bind(
    "<Return>",
    lambda event: search_from_bar()
)


# ---------------------------------------------------------
# SEARCH BUTTON
# ---------------------------------------------------------

search_button = tk.Button(
    search_frame,
    text="🔎 SEARCH",
    font=("Arial", 11, "bold"),
    padx=18,
    pady=9,
    cursor="hand2",
    command=search_from_bar
)

search_button.grid(
    row=0,
    column=2,
    padx=(10, 0)
)


# =========================================================
# RESULTS
# =========================================================

results_label = tk.Label(
    main_frame,
    text="🔎 YouTube Results",
    font=("Arial", 14, "bold")
)

results_label.grid(
    row=1,
    column=0,
    sticky="w",
    pady=(5, 3)
)


result_frame = tk.Frame(
    main_frame,
    relief="groove",
    bd=1
)

result_frame.grid(
    row=2,
    column=0,
    sticky="nsew"
)

result_frame.columnconfigure(
    0,
    weight=1
)

result_frame.rowconfigure(
    0,
    weight=1
)


result_list = tk.Listbox(
    result_frame,
    font=("Arial", 11),
    selectmode=tk.SINGLE
)

result_list.grid(
    row=0,
    column=0,
    sticky="nsew",
    padx=8,
    pady=8
)


result_scrollbar = ttk.Scrollbar(
    result_frame,
    orient="vertical",
    command=result_list.yview
)

result_scrollbar.grid(
    row=0,
    column=1,
    sticky="ns",
    pady=8
)

result_list.config(
    yscrollcommand=result_scrollbar.set
)


# ---------------------------------------------------------
# SELECT BUTTON
# ---------------------------------------------------------

select_button = tk.Button(
    main_frame,
    text="✅ SELECT RESULT",
    font=("Arial", 10, "bold"),
    padx=18,
    pady=8,
    cursor="hand2",
    command=select_result
)

select_button.grid(
    row=3,
    column=0,
    pady=8
)


# =========================================================
# DOWNLOAD OPTIONS
# =========================================================

download_frame = tk.LabelFrame(
    main_frame,
    text="⬇ Download Options",
    font=("Arial", 12, "bold")
)

download_frame.grid(
    row=4,
    column=0,
    sticky="ew",
    pady=8
)

download_frame.columnconfigure(
    1,
    weight=1
)


# ---------------------------------------------------------
# FORMAT
# ---------------------------------------------------------

tk.Label(
    download_frame,
    text="Format:",
    font=("Arial", 10, "bold")
).grid(
    row=0,
    column=0,
    padx=10,
    pady=9
)


format_menu = ttk.Combobox(
    download_frame,
    textvariable=download_mode,
    values=[
        "Audio (MP3)",
        "Video (MP4)"
    ],
    state="readonly",
    width=20
)

format_menu.grid(
    row=0,
    column=1,
    sticky="w",
    padx=5,
    pady=9
)


# ---------------------------------------------------------
# FOLDER
# ---------------------------------------------------------

tk.Label(
    download_frame,
    text="Save folder:",
    font=("Arial", 10, "bold")
).grid(
    row=1,
    column=0,
    padx=10,
    pady=9
)


folder_entry = tk.Entry(
    download_frame,
    textvariable=folder_var,
    font=("Arial", 10)
)

folder_entry.grid(
    row=1,
    column=1,
    sticky="ew",
    padx=5,
    pady=9
)


browse_button = tk.Button(
    download_frame,
    text="📁 Browse",
    command=choose_folder,
    cursor="hand2"
)

browse_button.grid(
    row=1,
    column=2,
    padx=10,
    pady=9
)


# =========================================================
# DOWNLOAD BUTTON
# =========================================================

download_button = tk.Button(
    main_frame,
    text="⬇ DOWNLOAD",
    font=("Arial", 13, "bold"),
    padx=30,
    pady=11,
    cursor="hand2",
    command=download_current
)

download_button.grid(
    row=5,
    column=0,
    pady=10
)


# =========================================================
# PROGRESS
# =========================================================

progress_label = tk.Label(
    main_frame,
    text="",
    font=("Arial", 10)
)

progress_label.grid(
    row=6,
    column=0,
    pady=3
)


# =========================================================
# STATUS
# =========================================================

status = tk.Label(
    main_frame,
    text="Ready. Individual Download mode.",
    font=("Arial", 10),
    justify="left",
    anchor="w"
)

status.grid(
    row=7,
    column=0,
    sticky="ew",
    pady=5
)


# =========================================================
# KEYBOARD SHORTCUT
# =========================================================

window.bind(
    "<Control-f>",
    lambda event: search_entry.focus_set()
)


# =========================================================
# START
# =========================================================

window.mainloop()