from flask import Flask, jsonify, make_response, render_template, request, send_file
from flask_cors import CORS, cross_origin
import base64
import json
from services import utils
from services import pornhub

app = Flask(__name__, static_url_path='/',
            static_folder='templates', template_folder='templates')
CORS(app)

# a: filmes e séries
# b: roms de jogos clássicos
# c: torrent de jogos
# d: cursos
# e: apks
# f: mp4 download
# g: mp3 download
# h: animes online

latests = {
    'a': pornhub.get_latest_videos,
}

searchs = {
    'a': pornhub.search_video,
}

downloads = {
    'a': pornhub.get_episodio_link,
}

categories = {
    'l': latests,
    's': searchs,
    'd': downloads,
}

@app.route('/')
def init():
    return render_template('index.html')

@app.route('/graphql', methods=['POST'])
def graphql():
    try:
        header = request.headers
        data = json.loads(base64.b64decode(header['Authorization'].replace('Bearer ', '')))
        category = categories[data['category']]
        if 'l' in data['category']:
            res = category[data['type']]()
        if 's' in data['category']:
            res = category[data['type']](data['search']) 
        if 'd' in data['category'] or 'v' in data['category']:
            if utils.isBase64(data['id']):
                data['id'] = base64.b64decode(data['id']).decode('utf-8')
            res = category[data['type']](data['id'])
            if len(res):
                if data['type'] == 'f': return send_file('./files/' + res, mimetype='video/mp4', as_attachment=True)
                if data['type'] == 'g': return send_file('./files/' + res, mimetype='audio/mpeg', as_attachment=True, download_name=str(res))
        return jsonify({'message': 'success', 'data': res})
    except Exception as e:
        print(e)
        return make_response('Server error', 500)

@app.after_request 
def after_request_callback(response):
    headers = response.headers
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)