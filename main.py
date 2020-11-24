from flask import Flask, render_template, request, flash
from flask_socketio import SocketIO
import numpy as np 

import hill_cipher as hc
from utils import process_key

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

messages = []

# key_matrix = np.array([[8,6,9,5],[6,9,5,10],[5,8,4,9],[10,6,11,4]])

@app.route('/', methods=['GET', 'POST'])
def sessions():
    if request.method == "POST":
        key_matrix = process_key(request.form.get('key'))
        if(not hc.check_key(key_matrix)):
            flash("Invalid Key: Key used is not invertible mod 26","danger")
            print()
            return render_template('session.html', messages=messages)
        decrypted_messages = []
        for msg in messages:
            dm = {}
            dm['user_name'] = msg['user_name']
            dm['message'] = hc.decrypt(msg['message'], key_matrix, msg['extra'])
            decrypted_messages.append(dm)
        return render_template('session.html', messages=decrypted_messages)
    else:
        return render_template('session.html', messages=messages)

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(response, methods=['GET', 'POST']):
    key_matrix = process_key(response['key'])
    encrypted_text, extra = hc.encrypt(response['message'], key_matrix)
    
    message = {}
    message['user_name'] = response['user_name']
    message['message'] = encrypted_text
    message['extra'] = extra
    if(not hc.check_key(key_matrix)):
        message['message'] = 'Invalid key: Key used is not invertible mod 26. Message not sent!'
        socketio.emit('my response', message, callback=messageReceived)
        return
    messages.append(message)
    print(response)
    socketio.emit('my response', message, callback=messageReceived)

if __name__ == '__main__':
    socketio.run(app)