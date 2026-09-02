# KuroiYFetch

> A simple, lightweight desktop application for searching and downloading YouTube media for offline use.

## 📌 About

**KuroiYFetch** is a Python-based desktop application built with **Tkinter** and **yt-dlp**.

The project was created as a learning project to practice GUI development, file handling, multithreading, external libraries, and media downloading with Python.

## ✨ Features

- 🔎 Search YouTube videos by name
- 🔗 Download directly using a YouTube URL
- 🎵 Download audio as MP3
- 🎬 Download video as MP4
- 📦 Bulk download multiple videos
- 📄 Load video names or URLs from `songs.txt`
- 📁 Choose a custom download folder
- 📊 Real-time download progress
- 🧵 Background downloading using Python threading
- 🖥️ Resizable Tkinter interface
- 💾 Save search results to `playlist.txt`

## 🛠️ Technologies Used

- **Python** — Main programming language
- **Tkinter** — Graphical User Interface
- **yt-dlp** — YouTube media extraction and downloading
- **FFmpeg** — Audio/video processing and format conversion
- **Threading** — Background download operations

## 📂 Project Structure

```text
KuroiYFetch/
│
├── gui.py
├── youtube.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── songs.txt
└── playlist.txt
````

## ⚙️ Installation

Follow the steps below to set up **KuroiYFetch** on your computer.

### 1. Install Python

Install Python on your computer if it is not already installed.

During installation on Windows, make sure to enable:

```text
Add Python to PATH
```

Check whether Python is installed:

```bash
python --version
```

### 2. Download KuroiYFetch

Clone this repository using Git:

```bash
git clone https://github.com/kuroi75/KuroiYFetch.git
```

Enter the project folder:

```bash
cd KuroiYFetch
```

Alternatively, you can download the repository as a ZIP file from GitHub and extract it.

### 3. Install Python Dependencies

Open **CMD** or a terminal inside the KuroiYFetch folder and run:

```bash
pip install -r requirements.txt
```

### 4. Install FFmpeg

KuroiYFetch requires **FFmpeg** for audio/video processing and merging.

FFmpeg is an external program and is **not installed through `requirements.txt`**.

After installing FFmpeg, verify the installation:

```bash
ffmpeg -version
```

If the terminal displays FFmpeg version information, FFmpeg is installed correctly.

### 5. Run KuroiYFetch

Run:

```bash
python gui.py
```

The KuroiYFetch GUI should now open.

## 📦 Bulk Download

KuroiYFetch supports downloading multiple videos or audio files using `songs.txt`.

Add one video name or YouTube URL per line:

```text
Avicii - Wake Me Up
Imagine Dragons - Demons
https://www.youtube.com/watch?v=example
```

Then open KuroiYFetch and switch to **Bulk Download** mode.

## 🎵 Download Modes

### Individual Download

Enter either:

* A YouTube video URL
* A song/video name

KuroiYFetch will search YouTube when a name is provided and allow you to select the desired result.

### Bulk Download

Use `songs.txt` to provide multiple video names or YouTube URLs.

KuroiYFetch will process the list automatically.

## ⚠️ Copyright & Legal Notice

**KuroiYFetch is intended for educational and personal use.**

This software is provided as a tool for learning about Python, GUI development, file handling, multithreading, external libraries, and media processing.

Users are solely responsible for ensuring that their use of this software complies with:

* Applicable copyright laws
* YouTube's Terms of Service
* The rights of content creators and copyright holders

**Do not use KuroiYFetch to download, reproduce, distribute, or otherwise use copyrighted material without the appropriate rights or permission.**

The developer does **not** encourage, promote, or endorse copyright infringement.

Downloading or using certain content may be restricted by copyright law, YouTube's Terms of Service, or other applicable regulations.

**Only download content that you have the legal right or permission to download.**

## 🎓 Educational Purpose

KuroiYFetch was developed as a **CSE learning project** to explore:

* Python programming
* Tkinter GUI development
* Multithreading
* File handling
* External Python libraries
* FFmpeg integration
* Error handling
* Project organization
* Software documentation

---

**Made with Python 🐍 by Kuroi**

````
