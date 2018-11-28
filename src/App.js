import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import axios from 'axios';
import YouTube from 'react-youtube';

class App extends Component {
  constructor(props){
    super(props)
    this.state = {
      reload:false,
      playlist:[],
      playing:null
    }
  }

  updatePlaylist(){
    axios.get('/gettop')
    .then(res=>{
      let playing_list = res.data
      let playing_array = []
      let currentPlay = null
      for(let i =0;i<playing_list.length;i++){
        let play_video = playing_list[i][0].split("v=")
        if(playing_list[i][0].includes('youtube')&& play_video.length === 2){
          if(!currentPlay){
            currentPlay = play_video[1]
          }
          playing_array.push(playing_list[i][0])
        }
      }
      this.setState({
        playlist:playing_array,
      })
    })
  }

  componentWillMount(){
    this.updatePlaylist()
    if(!this.state.reload){
      axios.post('/lst')
      .then(()=>{
        this.updatePlaylist()
      })
      .then(()=>{
        this.setState({
          reload:true
        })
      })
    }
  }


  UNSAFE_componentWillUpdate(nextProps, nextState){
    console.log(nextState)
    if(nextState.playlist.length > 0 && nextState.reload === false){
      console.log('hi')
      this.changeVideo(nextState.playlist[0])
      this.setState({
        reload:true
      })
    }
  }

  sendPlaylist(){
    let fd = new FormData()
    let play = this.state.playlist

    fd.append('song',document.getElementById("song").value)
    console.log(fd)
    axios.post('/song', fd)
      .then(res => console.log(res.data), err => {
        console.error(err)
        alert('Send failed')
      })
  }

  changeVideo(link){
    let playing_array = link.split("v=")
    let playing = playing_array[playing_array.length-1]
    this.setState({
      playing:playing
    })
  }

  render() {
    setTimeout(() => {this.updatePlaylist()}, 1000)
    return (
      <div className="App">
        <div className="Playlist">
          <div style={{flex:1}}>
            <h2 className="PlaylistHeader"> Playlist</h2>
            {this.state.playlist.map(link=>
              <p  
                className="App-link"
                onClick={()=>this.changeVideo(link)}
              >
                {link}
              </p>)
            }
          </div>
        </div>
        <div className="App-header">
          <h3>Musico Playlist</h3>
          <YouTube
            videoId={this.state.playing}
            opts={{
              height:'360',
              width:'640'
            }}
          />
          <input
            className="App-textarea"
            type='text'
            id="song"
            placeholder="youtube url"
          />
          <button 
            className="App-button"
            // type="submit"
            // value="submit"
            onClick={()=>this.sendPlaylist()}
          >
            send link
          </button>
        </div>
      </div>
    );
  }
}

export default App;
