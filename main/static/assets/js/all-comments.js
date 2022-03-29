let skip = 10;

$("#main-form").submit(function (e) {

    // preventing from page reload and default actions
    e.preventDefault();

    jsonData = {
        'skip': skip,
        'csrfmiddlewaretoken': document.getElementsByName('csrfmiddlewaretoken')[0].value,
    }

    
    // make POST ajax call
    $.ajax({
        type: 'POST',
        url: '/comments_api/',
        data: jsonData,
        success: function (response) {
            skip += 10;
            display_new_comments(response['comments']);

        },
        error: function (response) {
            alert('error');
        }
    })
})

function display_new_comments(comments) {
    comments.forEach(function (comment) {

        $('#comments-section').append(`
        <div class="table-responsive p-0">
        <tr>
            <td>
                <div class="d-flex px-2 py-1">
                    <div>
                        <img src="/static${comment.user_profile_photo}"
                            class="avatar avatar-sm me-3" alt="user1">
                    </div>
                    <div class="d-flex flex-column justify-content-center">
                        <h6 class="mb-0 text-sm">${comment.username}</h6>
                    </div>
                </div>
            </td>

            <td>${comment.comment}</td>
            <br>
            <td>
                <p style="font-size: 14px;">${getDateFormated(new Date(comment.date))}</p>
            </td>
            <hr>

        </tr>
        </tbody>
        </table>
        </div>`);
    });
}