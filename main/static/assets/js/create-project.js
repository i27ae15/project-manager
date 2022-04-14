let numDevelopers = 1;
let numObjectives = 1;
let numSubObjectives = 0;
let subObjectives = [0];
let developers = {};

$.ajax({
    type: 'GET',
    url: '/get-users/',
    success: function (response) {
        developers = response.users;
    },
    error: function (response) {
        alert('An error has ocurred, probably you are not connected to the internet, please reload the page.');
    }
})

// ------------------------------------------------------------------------------------
// Developers
// ------------------------------------------------------------------------------------

function addDeveloper() {

    numDevelopers++;

    $('#add-developers').append(`
    <div id="developer-${numDevelopers - 1}" class="developers" name="${numDevelopers - 1}">
        <div class="row" id="add-developers">

            <div class="col-lg-5">
                <div class="mb-3">
                    <label for="developer" class="form-label">Developer</label>
                    <select class="form-control" id="select-developer-${numDevelopers - 1}" name="developer-${numDevelopers - 1}-id">
                    </select>
                </div>
            </div>

            <div class="col-lg-5">
                <div class="mb-3">
                    <label for="developer" class="form-label">Role - Leave it blank to
                        not change it</label>
                    <select class="form-control" id="role-developer-${numDevelopers - 1}" name="role-developer-${numDevelopers - 1}">

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
                            type="button" onclick="deleteDeveloper(${numDevelopers - 1})">Delete</button>
                </div>
            </div>
        </div>
    </div>
    `)

    for (let n=0; n < developers.length; n++) {
        d = `${developers[n].first_name} ${developers[n].last_name} - ${developers[n].username} - ${developers[n].role}`
        $(`#select-developer-${numDevelopers - 1}`).append(
            $('<option>', {
                value: developers[n].user_id,
                text: d,
            }));
    }

}


function deleteDeveloper(developerNumber) {
    $(`#developer-${developerNumber}`).remove();
}

// ------------------------------------------------------------------------------------
//  Objectives 
// ------------------------------------------------------------------------------------

function createObjective(){
    numObjectives++;
    subObjectives.push(0);

    $('#objectives').append(`
    <div id="objective-${numObjectives - 1}" name="${numObjectives - 1}" class="objectives">
        <div class="row">
            <div class="px-2 col-lg-6 mb-3">
                <label class="form-label">Objective</label>
                <input type="text" class="form-control" id="objective-${numObjectives - 1}-name" name="objective-${numObjectives - 1}-name" required>
            </div>

            <div class="px-2 col-lg-3 mb-3">
                <label class="form-label">Deadline</label>
                <input type="date" class="form-control" id="objective-${numObjectives - 1}-deadline" name="objective-${numObjectives - 1}-deadline" required>
            </div>

            <div class="px-2 col-lg-3 mb-3">
                <label class="form-label">Delete all sub-objectives</label>
                <button class="btn btn-danger w-100" type="button" onclick="deleteObjective(${numObjectives - 1})">Delete
                </button>       
            </div>
        </div>

        <div id="objective-${numObjectives - 1}-sub-objectives">

        </div>

        <div class="row">
            <div class="px-2 col-lg-5 mb-3">
                <button type="button" class="btn btn-warning w-100 mt-2" onclick="createSubObjective(${numObjectives - 1})">
                    Create new sub-objective
                </button>
            </div>
        </div>

    </div>
    `)
}


function deleteObjective(obj){
    $(`#objective-${obj}`).remove();
}

// ------------------------------------------------------------------------------------
// Sub-objectives
// ------------------------------------------------------------------------------------

function createSubObjective(parent){

    $(`#objective-${parent}-sub-objectives`).append(`
    <div id="objective-${parent}-sub-objective-${subObjectives[parent]}">
        <div class="row">
            <div class="px-2 col-lg-6 mb-3">
                <label class="form-label">Sub-objective</label>
                <input type="text" class="form-control sub-objective-${parent}-name" required>
            </div>

            <div class="px-2 col-lg-3 mb-3">
                <label class="form-label">Deadline</label>
                <input type="date" class="form-control sub-objective-${parent}-deadline" required>
            </div>

            <div class="px-2 col-lg-3 mb-3">
                <label class="form-label">Delete</label>
                <button class="btn btn-danger w-100" type="button" onclick="deleteSubObjective(${parent}, ${subObjectives[parent]})">Delete</button>       
            </div>
        </div>
    </div>
    `);

    subObjectives[parent]++;
}


function deleteSubObjective(parent, subObj){
    $(`#objective-${parent}-sub-objective-${subObj}`).remove();
}


// ------------------------------------------------------------------------------------
// Get data from inputs 
// ------------------------------------------------------------------------------------


function getObjectives(){
    let objectives = [];
    let arrayOfObjectives = $('.objectives');

    for (let obj = 0; obj < arrayOfObjectives.length; obj++) {
        let objectiveID = arrayOfObjectives[obj].attributes.name.value;

        let subObjectivesNames = $(`.sub-objective-${objectiveID}-name`);
        let subObjectivesDeadlines = $(`.sub-objective-${objectiveID}-deadline`);
        let currentSubObjectives = [];
        
        for (let i = 0; i < subObjectivesNames.length; i++){
            let newSubObjective = {
                'sub_objective': subObjectivesNames[i].value,
                'deadline': subObjectivesDeadlines[i].value,
            }

            currentSubObjectives.push(newSubObjective);
        }

        let newObjective = {
            'objective': $(`#objective-${objectiveID}-name`).val(),
            'deadline': $(`#objective-${objectiveID}-deadline`).val(),
            'sub_objectives': currentSubObjectives,
        };

        objectives.push(newObjective);

    }   

    return objectives;
}


function getDevelopers(){
    let developers = []

    let developersObjects = $('.developers');

    for (let dev = 0; dev < developersObjects.length; dev++){

        let developerFrontendID = developersObjects[dev].attributes.name.value;
        
        let newDeveloper = {
            'id': $(`#select-developer-${developerFrontendID}`).val(),
            'role': $(`#role-developer-${developerFrontendID}`).val(),
        }

    
        developers.push(newDeveloper);
    }
    
    return developers
}

// ------------------------------------------------------------------------------------
// Create project form
// ------------------------------------------------------------------------------------


$('#create-project-form').submit(function (e) {

    // preventing from page reload and default actions
    e.preventDefault();

    jsonData = {
        'project_name': $('#project-name').val(),
        'project_resume': $('#project-resume').val(),
        'project_deadline': $('#project-deadline').val(),
        'project_manager': $('#project-manager').val(),
        'objectives': getObjectives(),
        'developers': getDevelopers(),
        'csrfmiddlewaretoken': document.getElementsByName('csrfmiddlewaretoken')[0].value,
    }

    console.log(jsonData)

    $.ajax({
        type: 'POST',
        url: '',
        data: jsonData,
        success: function (response) {

        },
        error: function (response) {
            alert('An error has ocurred with your message, please try again.');
        }
    })

})
