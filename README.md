# KuroiYFetch

> A simple, lightweight desktop application for searching and downloading
> YouTube media for offline use.

## 📌 About

**KuroiYFetch** is a Python-based desktop application built with Tkinter
and yt-dlp.

The project was created as a learning project to practice GUI development,
file handling, multithreading, external libraries, and media downloading
with Python.

## ✨ Features

- 🔎 Search YouTube videos by name
- 🔗 Download directly using a YouTube URL
- 🎵 Download audio as MP3
- 🎬 Download video as MP4
- 📦 Bulk download multiple videos
- 📄 Load and save download lists using `songs.txt`
- 📁 Choose a custom download folder
- 📊 Real-time download progress
- 🧵 Background downloading using Python threading
- 🖥️ Resizable Tkinter interface
- 💾 Save search results to `playlist.txt`

## 🛠️ Technologies Used

- **Python**
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
