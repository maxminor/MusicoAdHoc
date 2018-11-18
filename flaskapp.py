from flask import Flask, jsonify
import _thread
from adhoc import UDPAdHoc

adhocListener = UDPAdHoc(ip="0.0.0.0", port=5000)
app = Flask(__name__)

@app.route("/")
def hello():
    return jsonify(adhocListener.song_data)

if __name__ == '__main__':
    _thread.start_new_thread(adhocListener.listenUDP, tuple())
    _thread.start_new_thread(app.run(host="0.0.0.0", port=8080),())
