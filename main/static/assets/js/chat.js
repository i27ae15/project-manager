let profilePhoto = $('#profile-photo').val()
let username = $('#username').val()

$('#send-message-form').submit(function (e) {

    // preventing from page reload and default actions
    e.preventDefault();
    let chatId = $('#chat-id');
    let userId = $('#user-id');
    let text_input = $('#text-input');

    jsonData = {
        'chat_id': chatId.val(),
        'user_id': userId.val(),
        'text': text_input.val(),
        'csrfmiddlewaretoken': document.getElementsByName('csrfmiddlewaretoken')[0].value,
    }

    let regExp = /[a-zA-Z]/g;
    let specialChars = /[`!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?~]/;


    if (!regExp.test(jsonData.text) && !specialChars.test(jsonData.text)){
        return 
    } 

    $.ajax({
        type: 'POST',
        url: '/send_message_api/',
        data: jsonData,
        success: function (response) {
            addNewMessage(jsonData.text)
            text_input.val('')
        },
        error: function (response) {
            alert('An error has ocurred with your message, please try again.');
        }
    })

})

function addNewMessage(text, right = true) {

    let date = getDateFormated(new Date);

    if (right) {
    $('#chat-messages').append(`
    <div class="chat-message-right pb-4">
        <div>
            <img src="${'/static' + profilePhoto}" class="rounded-circle mr-1" alt="${username}"
                width="40" height="40">

        </div>
        <div class="flex-shrink-1 bg-light rounded py-2 px-3 mr-3">
            <div class="font-weight-bold mb-1">You</div>
            ${text}
            <div class="text-muted small text-nowrap mt-2">${date}</div>
        </div>
    </div>
    `)
    }
}