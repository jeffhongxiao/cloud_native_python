import sqlite3

from flask import Flask, jsonify, request, abort, make_response

app = Flask(__name__)


@app.route("/api/v1/info")
def home_index():
    conn = sqlite3.connect('mydb.db')
    print("Opened database successfully")
    api_list = []
    cursor = conn.execute(
        "SELECT buildtime, version, methods, links from apirelease")
    for row in cursor:
        api = {}
        api['version'] = row[0]
        api['buildtime'] = row[1]
        api['methods'] = row[2]
        api['links'] = row[3]
        api_list.append(api)
    conn.close()
    return jsonify({'api_version': api_list}), 200


@app.route("/api/v1/users", methods=['GET'])
def get_users():
    return list_users()


def list_users():
    conn = sqlite3.connect('mydb.db')
    api_list = []
    cursor = conn.execute(
        'SELECT username, full_name, email, password, id from users'
    )

    for row in cursor:
        a_dict = {}
        a_dict['username'] = row[0]
        a_dict['name'] = row[1]
        a_dict['email'] = row[2]
        a_dict['password'] = row[3]
        a_dict['id'] = row[4]
        api_list.append(a_dict)

    conn.close()
    return jsonify({'user_list': api_list})


@app.route("/api/v1/users/<int:user_id>", methods=['GET'])
def get_user(user_id):
    return list_user(user_id)


def list_user(user_id):
    conn = sqlite3.connect('mydb.db')
    cursor = conn.execute(
        'SELECT username, full_name, email, password, id from users where id=?', (
            user_id,)
    )
    data = cursor.fetchall()

    if len(data) == 0:
        abort(404)
    else:
        user = {}
        user['username'] = data[0][0]
        user['name'] = data[0][1]
        user['email'] = data[0][2]
        user['password'] = data[0][3]
        user['id'] = data[0][4]

    conn.close()
    return jsonify(user)


@app.route('/api/v1/users', methods=['POST'])
def create_user():
    if not request.json:
        abort(400)
    if not 'username' in request.json:
        abort(400)
    if not 'email' in request.json:
        abort(400)
    if not 'password' in request.json:
        abort(400)

    user = {
        'username': request.json['username'],
        'email': request.json['email'],
        'name': request.json.get('name', ''),
        'password': request.json['password']
    }

    return jsonify({'status': add_user(user)}), 201


def add_user(new_user):
    conn = sqlite3.connect('mydb.db')

    cursor = conn.cursor()

    cursor.execute('SELECT * from users where username=? or email=?',
                   (new_user['username'], new_user['email']))

    data = cursor.fetchall()

    if len(data) != 0:
        abort(409)

    cursor.execute('INSERT INTO users (username, email, password, full_name) values (?,?,?,?)',
                   (new_user['username'], new_user['email'], new_user['password'], new_user['name']))
    conn.commit()
    conn.close()

    return 'Success'
    # return jsonify({})


@app.route('/api/v1/users', methods=['DELETE'])
def delete_user():
    if not request.json:
        abort(400)
    if not 'username' in request.json:
        abort(400)

    username = request.json['username']
    return jsonify({'status': del_user(username)}), 200


def del_user(username):
    conn = sqlite3.connect('mydb.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * from users WHERE username=?', (username,))

    data = cursor.fetchall()

    if len(data) == 0:
        abort(404)

    cursor.execute('DELETE FROM users WHERE username==?', (username,))
    conn.commit()
    conn.close()

    return 'Success'


@app.route('/api/v1/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    if not request.json:
        abort(400)

    user = {'id': user_id}

    key_list = request.json.keys()
    for key in key_list:
        user[key] = request.json[key]

    print(user)

    return jsonify({'status': upd_user(user)}), 200


def upd_user(user):
    conn = sqlite3.connect('mydb.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * from users where id = ?', (user['id'],))
    data = cursor.fetchall()

    if len(data) == 0:
        abort(404)

    key_list = user.keys()
    for key in key_list:
        print(user, key)
        cursor.execute('''UPDATE users set {0} = ? where id = ?'''.format(
            key), (user[key], user['id']))

    conn.commit()
    return 'Success'

@app.route('/api/v2/tweets', methods=['GET'])
def get_tweets():
    print('get_tweets()')
    return list_tweets()

def list_tweets():
    conn = sqlite3.connect('mydb.db')
    api_list = []

    cursor = conn.execute('SELECT username, body, tweet_time, id FROM tweets')
    data = cursor.fetchall()
    
    for row in data:
        tweet = {}
        tweet['Tweet by'] = row[0]
        tweet['Body'] = row[1]
        tweet['Timestamp'] = row[2]
        tweet['id'] = row[3]
        api_list.append(tweet)

    conn.close()
    return jsonify({'tweet_list': api_list})

@app.errorhandler(400)
def invalid_request(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.errorhandler(409)
def user_found(error):
    return make_response(jsonify({'error': 'Conflict! Record exist'}), 409)


@app.errorhandler(404)
def resource_not_found(error):
    return make_response(jsonify({'error': 'Resource not found!'}), 404)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
