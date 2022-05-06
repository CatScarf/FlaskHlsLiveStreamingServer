import flask

from generate_video import M3U8

app = flask.Flask(__name__)

# @app.route('/')
# def index():
#     return flask.render_template('index.html')

@app.route('/video/<string:path>')
def stream(path):
    directory = './video'
    return flask.send_from_directory(directory=directory, path=path)

if __name__ == '__main__':
    m3u8 = M3U8(duration=3, max_cache=180, del_old_second=180)
    app.run()