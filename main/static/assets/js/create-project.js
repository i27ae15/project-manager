let numDevelopers = 1;
let developers = {};

// preventing from page reload and default actions

// jsonData = {
//     'csrfmiddlewaretoken': document.getElementsByName('csrfmiddlewaretoken')[0].value,
// }

$.ajax({
    type: 'GET',
    url: '/get-users/',
    success: function (response) {
        developers = jsonData.text;
        console.log(developers);
    },
    error: function (response) {
        alert('An error has ocurred, probably you are not connected to the internet, please reload the page.');
    }
})



function addDeveloper() {

    numDevelopers++;

    $('#add-developers').append(`
    <div id="developer-${numDevelopers}">
        <div class="row" id="add-developers">

            <div class="col-lg-5">
                <div class="mb-3">
                    <label for="developer" class="form-label">Developer</label>
                    <select class="form-control" id="select-developer-${numDevelopers}">
                    </select>
                </div>
            </div>

            <div class="col-lg-5">
                <div class="mb-3">
                    <label for="developer" class="form-label">Role - Leave it blank to
                        not change it</label>
                    <select class="form-control" id="role-developer-${numDevelopers}">

                    <option></option>
                    <option value="Full stack">Fullstack</option>
                    <option value="Frontend">Frontend</option>
                    <option value="Backend">Backend</option>

                    </select>
                </div>
            </div>

            <div class="col-lg-2">
                <div class="mb-3">
                    <label for="delete-developer" class="form-label"> Delete <label>
                            <button class="btn btn-danger w-100 mt-2"
                            type="button" onclick="deleteDeveloper(${numDevelopers})">Eliminate</button>
                </div>
            </div>
        </div>
    </div>
`)


    developers.forEach(developer => {
        d = `${developer.first_name} ${developer.last_name} - ${developer.username} - ${developer.role}`
        $(`#select-developer-${numDevelopers}`).append(
            $('<option>', {
                value: d,
                text: d,
            }));

    });

    
        

}

function deleteDeveloper(developerNumber) {
    $(`#developer-${developerNumber}`).remove()
}