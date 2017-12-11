const fs = require('fs')
const audio = require('web-audio-api')
const Speaker = require('speaker')

const context = new audio.AudioContext()
context.outStream = new Speaker({
  channels: context.format.numberOfChannels,
  bitDepth: context.format.bitDepth,
  sampleRate: context.sampleRate
})

fs.readFile(process.argv[2], function (err, buf) {
  if (err) throw err

  context.decodeAudioData(buf, function (audioBuffer) {
    const bufferNode = context.createBufferSource()
    bufferNode.connect(context.destination)
    bufferNode.buffer = audioBuffer
    bufferNode.loop = true
    bufferNode.start(0)
  })
})
