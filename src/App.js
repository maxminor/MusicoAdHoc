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

  componentWillMount(){
    axios.get('/gettop')
    .then(res=>{
      let playing_list = res
      let playing_array = []
      let currentPlay = null
      for(let i =0;i<playing_list.length;i++){
        let play_video = playing_list[i].split("v=")
        if(playing_list[i].includes('youtube')&&play_video.length == 2){
          if(!currentPlay){
            currentPlay = play_video[1]
          }
          playing_array.push(playing_list[i])
        }
      }
      this.setState({
        playlist:playing_array,
        playing:currentPlay
      })
    })
  }

  sendPlaylist(){
    let fd = new FormData()
    fd.append('song',document.getElementById("song").value)
    console.log(fd)
  }

  changeVideo(link){
    let playing_array = link.split("v=")
    let playing = playing_array[playing_array.length-1]
    this.setState({
      playing:playing
    })
  }

  render() {
    if(this.state.reload){
      setTimeout(() => {          
        this.setState({
          reload: false,
          playlist:['https://www.youtube.com/watch?v=y906Cldzg-4','https://www.youtube.com/watch?v=27kOE0ndy28']
        });
      }, 10000)
    }
    else{
      setTimeout(() => {
        this.setState({
          reload: true,
          playlist:['https://www.youtube.com/watch?v=y906Cldzg-4','https://www.youtube.com/watch?v=27kOE0ndy28']
        });
      }, 10000)
    }
    return (
      <div className="App">
        <div className="App-header">
          <h3>Musico Playlist</h3>
          <YouTube
            videoId={this.state.playing}
            opts={{
              height:'360',
              width:'640'
            }}
          />
          <div style={{margin:'0.5vw'}}>
            {this.state.playlist.map(link=>
              <p  
                className="App-link"
                onClick={()=>this.changeVideo(link)}
              >
                {link}
              </p>)
            }
          </div>
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
