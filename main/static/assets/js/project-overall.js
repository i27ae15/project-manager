function completeSubObjective(projectID, subID){

    jsonData = {
        'csrfmiddlewaretoken': document.getElementsByName('csrfmiddlewaretoken')[0].value,
        'sub_objective_id': subID,
        'projet_id': projectID
    }

    $.ajax({
        type: 'POST',
        url: '/complete-sub-objective/',
        data: jsonData,
        success: function (response) {

            $(`#btn-complete-sub-obj-${subID}`).remove()
            $(`#complete-on-${subID}`).append(`
                <div class="col-lg" style="text-align: center;">
                <div class="card h-100" >
                    <p>Waiting for approval...</p>
                </div>
            </div>`)
        },
        error: function (response) {
            alert('An error has ocurred, please try again.');
        }
    })

}