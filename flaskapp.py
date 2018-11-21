from flask import Flask, jsonify, request, send_from_directory
import os
import _thread
from adhoc import UDPAdHoc
import udpSender
import netifaces as ni

#THE HACKKKKKSSS
ssid = os.popen('iwconfig ' + ni.interfaces()[-1] + " | grep 'ESSID'" ).read().split()[-1][7:-1]
adhocListener = UDPAdHoc(network_name=ssid, ip="0.0.0.0", port=5000)
app = Flask(__name__, static_folder='build')


@app.route('/song', methods=['GET', 'POST'])
def setNewSong():
    if request.method == 'GET':
        return jsonify(adhocListener.song_data)
    elif request.method == 'POST':
        # adhocListener.addSong(request.form['song'])

        broadcastMessage = 'ADD ' + request.form['song']
        udpSender.sendUDPPacket('10.42.0.255', 5000, broadcastMessage)
        return jsonify({'message': 'song has been broadcasted'})


@app.route('/gettop')
def getTop3Music():
    return jsonify(adhocListener.getTopMusic(3))

@app.route('/network', methods=['GET', 'POST'])
def networks():
	if request.method == 'GET':
		return adhocListener.network_name
	elif request.method == 'POST':
		adhocListener.network_name = request.form['network_name']

		return 'network has been created'

@app.route('/reset', methods=['POST'])
def resetdata():
    if request.method == 'POST':
        adhocListener.resetData()
        return 'data has been reset'

@app.route('/lst', methods=['POST'])
def sendLST():
    if request.method == 'POST':
        adhocListener.requestSLS()
        _thread.start_new_thread(adhocListener.countdown, tuple())
        return 'SLS message has been sent'



@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    # print(path)
    if path != "" and os.path.exists("build/" + path):
        return send_from_directory('build', path)
    else:
        return send_from_directory('build', 'index.html')


if __name__ == '__main__':
    _thread.start_new_thread(adhocListener.listenUDP, tuple())
    _thread.start_new_thread(app.run(host="0.0.0.0", port=8080), ())
