from flask import Flask, jsonify, request
import _thread
from adhoc import UDPAdHoc
import udpSender

adhocListener = UDPAdHoc(ip="0.0.0.0", port=5000)
app = Flask(__name__)

@app.route('/song',methods=['POST'])
def setNewSong():
    if request.method == 'POST':
        adhocListener.addSong(request.form['song'])

        broadcastMessage = 'ADD ' + request.form['song']
        udpSender.sendUDPPacket('10.42.0.255', 5000, broadcastMessage)
        return jsonify({'message':'song has been added'})

@app.route('/gettop')
def getTop3Music():
    return jsonify(adhocListener.getTopMusic(3))

@app.route("/")
def hello():
    return jsonify(adhocListener.song_data)

if __name__ == '__main__':
    _thread.start_new_thread(adhocListener.listenUDP, tuple())
    _thread.start_new_thread(app.run(host="0.0.0.0", port=8080),())
