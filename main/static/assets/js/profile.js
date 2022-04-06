
function completeTask(){
    jsonData = {
        'csrfmiddlewaretoken': document.getElementsByName('csrfmiddlewaretoken')[0].value,
        'task_id': $('#task-id').val(),
        'username': $('#username').val(),
    }

    $.ajax({
        type: 'POST',
        url: '/complete-task/',
        data: jsonData,
        success: function (response) {
            $('#btn-complete-task').remove()
            $('#current-task-section').append(`
        <div class="col-lg" style="text-align: center;">
            <div class="card h-100" >
                <p>Waiting for approval...</p>
            </div>
        </div>
        `)
        },
        error: function (response) {
            alert('An error has ocurred, please try again.');
            console.log(response)
        }
    })
}