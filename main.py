import flask

from generate_video import M3U8

app = flask.Flask(__name__)

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/video/<string:path>')
def stream(path):
    directory = './video'
    return flask.send_from_directory(directory, path)

if __name__ == '__main__':
    m3u8 = M3U8(fps=60, duration=3, max_cache=10, del_old_seconds=180, ffmpeg='jrottenberg/ffmpeg')
    app.run()