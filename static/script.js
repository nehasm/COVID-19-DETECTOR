var speechRecognition = window.webkitSpeechRecognition

var recognition = new speechRecognition()

// var textbox = $("#textbox")

var instructions = $("#instructions")

var content = ""

recognition.continuous = true

recognition.onstart=function(){
    instructions.text("I am listening")
}

recognition.onspeechend=function(){
    instructions.text("I am unable to listen,please press start button to talk with me")
}

recognition.onerror=function(){
    instructions.text("There is error,please try again")
}

recognition.onresult=function(event){
    var current = event.resultIndex;
    var transcript = event.results[current][0].transcript
    content+=transcript
    document.getElementById('textbox').value=content
}


$('#start-btn').click(function (event){
    if(content.length){
        content+=""
    }
    recognition.start()
    console.log("start 1")
})
$('textbox').on('input',function(){
    content= $(this).val()
})