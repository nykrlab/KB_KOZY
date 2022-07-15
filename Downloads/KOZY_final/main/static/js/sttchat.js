window.SpeechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition;
const synth = window.speechSynthesis;
const recognition = new SpeechRecognition();
recognition.lang = "ko-KR";

const icon = document.querySelector('.record')
const outputYou = document.querySelector('#output-you');

icon.addEventListener('click', () => {
  console.log('clicked');
  dictate();
});

const dictate = () => {
  recognition.start();
  recognition.onresult = (event) => {
    const speechToText = event.results[0][0].transcript;
    
    outputYou.value = speechToText;
  }
}