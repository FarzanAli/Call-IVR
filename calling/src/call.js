import { Device } from '@twilio/voice-sdk';

const device = new Device('eyJhbGciOiJIUzI1NiIsImN0eSI6InR3aWxpby1mcGE7dj0xIiwidHlwIjoiSldUIn0.eyJqdGkiOiJTSzRjOGEyODBkNjM0N2FjZTc4ZGQzZmYyZDkwYjg3ODI5LTE3MTgxNDg0MDIiLCJncmFudHMiOnsidm9pY2UiOnsiaW5jb21pbmciOnsiYWxsb3ciOnRydWV9LCJvdXRnb2luZyI6eyJhcHBsaWNhdGlvbl9zaWQiOiJBUDllMGE2ZjRiZWFkNzM0N2E4NDJiMzY2N2ZlMjhkYTM0In19LCJpZGVudGl0eSI6InVzZXIifSwiaXNzIjoiU0s0YzhhMjgwZDYzNDdhY2U3OGRkM2ZmMmQ5MGI4NzgyOSIsImV4cCI6MTcxODE1MjAwMiwibmJmIjoxNzE4MTQ4NDAyLCJzdWIiOiJBQ2ZjZTBiZWUwNTg4NTVjNzA3ZjRjNTY5MGMyMmZlODUyIn0.XBlCeQw0czMrZl1yfcE7T4MJOqQCkEuxTIAGV0nquWw');

var currentCall;

let audioContext;
let mediaStreamDestination;
let audioStream;

export let makeCall = async () => {
  const call = await device.connect({
    params: {
      To: '+18887643771'
    }
  })

  currentCall = call

  call.on('accept', connection => {
    audioContext = new AudioContext();
    mediaStreamDestination = audioContext.createMediaStreamDestination();
    // Once the call is accepted, check if connection.mediaStream exists before piping
    if (connection.mediaStream) {
      connection.mediaStream.pipeTo(mediaStreamDestination);
      audioStream = mediaStreamDestination.stream;
      setupAudioRecording();
    } else {
      console.log('Connection media stream is not available.');
    }
  });
}

// Function to convert ArrayBuffer to Base64
function arrayBufferToBase64(arrayBuffer) {
  let binary = '';
  const bytes = new Uint8Array(arrayBuffer);
  const len = bytes.byteLength;
  for (let i = 0; i < len; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  return btoa(binary);
}

// Create a MediaRecorder to capture audio from the MediaStream
function setupAudioRecording() {
  if (!audioStream) {
    console.log('Audio stream not available yet');
    return;
  }
  console.log('here')
  let mediaRecorder = new MediaRecorder(audioStream);
  mediaRecorder.ondataavailable = function(event) {
    console.log('data available')
    // Convert each chunk of audio data to Base64
    const arrayBuffer = event.data.arrayBuffer();
    const base64Data = arrayBufferToBase64(arrayBuffer);
    console.log(base64Data); // Output: Base64 encoded audio data for the chunk
  };
  mediaRecorder.start();
}

export let endCall = async () => {
  if(currentCall){
    currentCall.disconnect()
    currentCall = NaN
  }
  else{
    console.log('No active call to end.')
  }
}

export let sendDigits = async (digit) => {
  if(currentCall){
    currentCall.sendDigits(digit.toString())
  }
  else{
    console.log('No active call to send digits to.')
  }
}