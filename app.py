import sqlite3
import hashlib
import flask
from flask import request, jsonify, g, abort

app = flask.Flask(__name__)
DATABASE = 'hashes.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def create_hash_digest_table():
    cur = get_db().cursor()
    create_table = """CREATE TABLE IF NOT EXISTS hashes (
    digest TEXT PRIMARY KEY,
    message TEXT
    );"""

    cur.execute(create_table)


def generate_hash(message: str) -> str:
    byte_message = message.encode('utf-8')
    hash_message = hashlib.sha256()
    hash_message.update(byte_message)
    digest = hash_message.hexdigest()
    return digest


def insert_digest(digest: str, message: str):
    cur = get_db().cursor()
    cur.execute("INSERT OR IGNORE INTO hashes VALUES (?, ?)",
                (digest, message))


def retrieve_message_with_digest(digest: str) -> str:
    cur = get_db().cursor()
    cur.execute("SELECT * FROM hashes WHERE digest = (?)", (digest,))
    message = cur.fetchone()
    if message is None:
        abort(404)
    else:
        return message[1]


@app.errorhandler(404)
def invalid_digest(error):
    return "404: hash does not exist", 404


@app.route('/messages/<digest>', methods=['GET'])
def parse_digest(digest: str):
    original_message = retrieve_message_with_digest(digest)
    return jsonify({"message": original_message})


@app.route('/messages/', methods=['POST'])
def parse_message():
    message_data = request.get_json()
    message = message_data['message']
    digest = generate_hash(message)
    insert_digest(digest, message)
    db = get_db()
    db.commit()
    return jsonify({"digest": digest})


if __name__ == '__main__':
    with app.app_context():
        create_hash_digest_table()
    app.run(debug=True, host='0.0.0.0', port=5000)
