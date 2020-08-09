function submit_message(message) {
    $.post( "/send_message", {message: message}, handle_response);

    function handle_response(data) {
      // append the bot repsonse to the div
      $('.chat-container').append(`
            <div class="chat-message col-md-5 offset-md-7 bot-message">
                ${data.message}
            </div>
      `)
      var msg = new SpeechSynthesisUtterance();
      msg.text = data.message;
      window.speechSynthesis.speak(msg);
      // remove the loading indicator
      $("#loading" ).remove();
    }
}
$('#target').on('submit', function(e){
    e.preventDefault();
    const textbox = $('#textbox').val()
    // return if the user does not enter any text
    if (!textbox) {
      return
    }

    $('.chat-container').append(`
        <div class="chat-message col-md-5 human-message">
            ${textbox}
        </div>
    `)

    // loading 
    $('.chat-container').append(`
        <div class="chat-message text-center col-md-2 offset-md-10 bot-message" id="loading">
            <b>...</b>
        </div>
    `)

    // clear the text input 
    $('#textbox').val('')
    document.getElementById("textbox").value = ""
    content = ""

    // send the message
    submit_message(textbox)
});
