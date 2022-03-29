let activityToRemove = 0;

$('#timeline-form').submit(function (e) {

    // preventing from page reload and default actions
    e.preventDefault();

    input_field = $('#id_activity');

    jsonData = {
        'activity': input_field.val(),
        'csrfmiddlewaretoken': document.getElementsByName('csrfmiddlewaretoken')[0].value,
    }

    $.ajax({
        type: 'POST',
        url: '/timeline_api/',
        data: jsonData,
        success: function (response) {
            addNewActivityInTimeline(jsonData.activity)
            input_field.val('')
        },
        error: function (response) {
            alert('An error has ocurred with your form, please try again.');
        }
    })

})

function addNewActivityInTimeline(activity) {
    let date = getDateFormated(new Date);

    $('.timeline').children().last().remove();
    $('.timeline').prepend(`<div class="timeline-block mb-3">
    <span class="timeline-step">
      <i class="ni ni-bell-55 text-success text-gradient"></i>
    </span>
    <div class="timeline-content">
      <h6 class="text-dark text-sm font-weight-bold mb-0">${activity}</h6>
      <p class="text-secondary font-weight-bold text-xs mt-1 mb-0">${date}</p>
    </div>
  </div>`);
}

