$(document).on("submit", "form", function (e) {
    e.preventDefault();
    e.stopImmediatePropagation();
    let form = $(this);
    let url = form.attr('action');
    $.ajax({
        type: "POST",
        url: url,
        data: {
            title: $('input[type=text]').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function (item) {
            let newTask = `
                <li class="list-group-item">
                    <label>
                    <input type="checkbox"
                           onchange='toggleMark(this,${ item['id'] })'>
                    ${ item['title'] }
                    </label>
                 <span  class="float-right text-danger"
                        onclick='deleteTask(this,${ item['id'] })'>X</span>
                </li>`
            $('ul').append(newTask);
            $('.no-tasks').hide()
            $('input[type=text]').val('')
        },
        error: function (error) {
            throw new Error(`Error!: ${error['statusText']}`);
        }
    });
});

function toggleMark(obj, id) {
    clickedTask = $(obj).parents('label');
    textDecoration = clickedTask.css('text-decoration-line');
    reqType = (textDecoration === 'line-through') ? 'uncomplete' : 'complete'
    $.ajax({
        type: 'POST',
        url: `/details/${reqType}/`,
        data: {
            id,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function (response) {
            clickedTask.toggleClass('completed');
        },
        error: function (error) {
            throw new Error(`Error!: ${error['statusText']}`);
        }
    })
}

function deleteTask(obj, id) {
    clickedTask = $(obj).parents('li');
    $.ajax({
        type: 'POST',
        url: '/details/delete/',
        data: {
            id,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function (response) {
            clickedTask.remove();
            $('li').length === 0 ? $('.no-tasks').show() : '';
        },
        error: function (error) {
            throw new Error(`Error!: ${error['statusText']}`);
        }
    })
}
