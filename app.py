from flask import Flask, jsonify, request

app = Flask(__name__)

tracks = []
next_id = 1

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

@app.route('/tracks', methods=['GET'])
def listar_musicas():
    return jsonify(tracks), 200

@app.route('/tracks/<int:track_id>', methods=['GET'])
def obter_musica(track_id):
    for t in tracks:
        if t['id'] == track_id:
            return jsonify(t), 200
    return jsonify({"erro": "Música não encontrada"}), 404

@app.route('/tracks', methods=['POST'])
def adicionar_musica():
    global next_id
    data = request.get_json()
    if not data:
        return jsonify({"erro": "JSON ausente"}), 400
    campos = ['titulo', 'artista', 'duracao']
    if not all(c in data and data[c] for c in campos):
        return jsonify({"erro": "Campos obrigatórios: titulo, artista, duracao"}), 400
    nova = {
        "id": next_id,
        "titulo": data['titulo'],
        "artista": data['artista'],
        "duracao": data['duracao'],
        "url": data.get('url', "")
    }
    tracks.append(nova)
    next_id += 1
    return jsonify(nova), 201

@app.route('/tracks/<int:track_id>', methods=['PUT'])
def atualizar_musica(track_id):
    data = request.get_json()
    if not data:
        return jsonify({"erro": "JSON ausente"}), 400
    for t in tracks:
        if t['id'] == track_id:
            for campo in ['titulo', 'artista', 'duracao', 'url']:
                if campo in data:
                    t[campo] = data[campo]
            return jsonify(t), 200
    return jsonify({"erro": "Música não encontrada"}), 404

@app.route('/tracks/<int:track_id>', methods=['DELETE'])
def deletar_musica(track_id):
    for t in tracks:
        if t['id'] == track_id:
            tracks.remove(t)
            return '', 204
    return jsonify({"erro": "Música não encontrada"}), 404

if __name__ == '__main__':
    app.run(debug=True)
