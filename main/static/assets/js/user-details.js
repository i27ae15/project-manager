const userInfo = $('#user-info');
const pullRequest = $('#user-pull-request');
const newTask = $('#user-new-task');

function activeUserInfo(){

    userInfo.removeClass('invisible');

    pullRequest.addClass('invisible');
    newTask.addClass('invisible');
}

function activePullRequest(){

    pullRequest.removeClass('invisible');

    userInfo.addClass('invisible');
    newTask.addClass('invisible');
}

function activeNewTask(){

    newTask.removeClass('invisible');

    pullRequest.addClass('invisible');
    userInfo.addClass('invisible');
}

$('#new-task-form').submit(function (e) {

    // preventing from page reload and default actions
    e.preventDefault();
    let taskt = $('#task-input');
    let details = $('#details-input');
    let userId = $('#user-id');

    jsonData = {
        'task': taskt.val(),
        'details': details.val(),
        'user_id': userId.val(),
        'csrfmiddlewaretoken': document.getElementsByName('csrfmiddlewaretoken')[0].value,
    }

    $.ajax({
        type: 'POST',
        url: '/new-task-manager/',
        data: jsonData,
        success: function (response) {
            addNewTask(jsonData);
            taskt.val('');
            details.val('');
            alert('success');
        },
        error: function (response) {
            alert('An error has ocurred with your message, please try again.');
        }
    })

})


function addNewTask(data){
    $('#tasks').prepend(`
    <div class="row">
    <div class="profile-nav col-md-3">
    </div>
    <div class="profile-info col-md-9">
        <div class="panel" style="text-align: center; padding: 3%; font-size: 16px;">

            <p>${data.task}</p>

        </div>

        <div class="panel" style="padding: 3%;">

            ${data.details}

            <hr>

            <i class="fas fa-clock fa-2x" style="color: #ffd400; margin: 1% 0 1% 3%;"></i>

        </div>
    </div>
</div>
`);
}
