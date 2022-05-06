# Flask HLS Live Streming Server

This is a simple python flask hls live streaming server example

## 1. Quik Start

### 1.1. Installing FFmpeg

FFmpeg must be installed and accessible via the `$PATH` environment variable.

Browse the "Installing FFmpeg" section of [this page](https://github.com/kkroening/ffmpeg-python)

### 1.2. Installing Python Libraries

```bash
$ pip install -r requirements.txt
```

### 1.3. Running main.py

```bash
$ python main.py
```

### 1.4 Play live video in the player

You can play the example video in a player that supports the hls protocol by entering the following address

http://127.0.0.1:5000/video/playlist.m3u8

If you have an Apple device, you can also enter this address in Safari. This is because the hls protocol was developed by apple.

## 2. Relevant documents

[HLS Live streaming documentation provided by apple](https://developer.apple.com/documentation/http_live_streaming/example_playlists_for_http_live_streaming/live_playlist_sliding_window_construction)