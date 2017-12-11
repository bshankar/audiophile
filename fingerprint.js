const fs = require('fs')
const audio = require('web-audio-api')

function getAudio (filename, cb) {
  // get audio from filesystem
  fs.readFile(filename, function (err, buf) {
    if (err) throw err

    const context = new audio.AudioContext()
    context.decodeAudioData(buf, audioBuffer => cb(audioBuffer))
  })
}

function convertToMono (audioBuffer) {
  // convert stereo audio to mono by averaging output of both speakers
  const data = audioBuffer._data
  for (let i = 0; i < data[0].length; ++i) {
    data[0][i] = (data[0][i] + data[1][i]) / 2
  }
  audioBuffer._data = data.slice(0, 1)
  return audioBuffer
}

