
function open_attend_edit_modal(event,blog_id){
    var url = $(event.target).attr('attend_edit_url');
    $.ajax({
            
            url: url,
            type: 'GET',
            headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{csrftoken}}',
            },
            success: function(xhr, ajaxOptions, thrownError){
                $('.modal-body').html(xhr.html_content);
                $('#exampleModal').modal('show');
            },
            error: function(xhr, status, error) {
                console.error('Error fetching edit form: ' + error);
            }
        });
}

$(document).ready(function() {
$('#exampleModal').on('submit', 'form', function(e) {
    e.preventDefault();
    $.ajax({
        type: $(this).attr('method'),
        url: $(this).attr('action'),
        data: $(this).serialize(),
        success: function(response) {
            alert(response.message);
            $('#exampleModal').modal('hide');
            window.location.href = window.location.href;
        }
    });

});
});