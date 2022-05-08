# Flask HLS Live Streming Server

This is a simple python flask hls live streaming server example

## 1. Quik Start

### 1.1. Cloning project

```bash
$ git clone https://github.com/CatScarf/FlaskHlsLiveStreamingServer.git
```

### 1.2. Installing FFmpeg

FFmpeg must be installed. I recommend that you use docker to install.

```bash
docker pull jrottenberg/ffmpeg
```

And make sure you can run `docker run jrottenberg/ffmpeg` in your terminal. If you have to use `sudo docker`, please add your user to the docker user group.

If you are using another docker image, please change the parameter `ffmpeg` to `IMAGENAME/ffmpeg` in the init parameter of class M3U8 in `main.py`. If you have installed ffmpeg without docker, please change this parameter to `ffmpeg`. Please note that your ffmpeg must contain the libx264 encoder. This is why I recommend that you use docker. Generally speaking installing ffmpeg without docker is a bit tricky, so I still recommend you use docker.

### 1.3. Installing Python Libraries

```bash
$ pip install -r requirements.txt
```

### 1.4. Running main.py

```bash
$ cd FlaskHlsLiveStreamingServer/
$ python main.py
```

### 1.5 Play live video in the player

You can directly visit the [http address](http://127.0.0.1:5000/) show in your terminal. This page uses the popular javasccript library [hls.js](https://github.com/video-dev/hls.js/tree/master/demo).

You can also play the example video in a player ([PotPlayer](https://potplayer.daum.net/) or [IINA](https://iina.io/)) that supports the hls protocol by entering the following address [http://127.0.0.1:5000/video/playlist.m3u8](http://127.0.0.1:5000/video/playlist.m3u8). If you have an Apple device, you can also enter this address in [Safari](https://www.apple.com/safari/). This is because the hls protocol was developed by apple.

## 2. Relevant documents

[HLS Live streaming documentation provided by apple](https://developer.apple.com/documentation/http_live_streaming/example_playlists_for_http_live_streaming/live_playlist_sliding_window_construction)