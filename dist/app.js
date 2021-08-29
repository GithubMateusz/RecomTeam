import '../sass/app.scss';
import './application/invite_player.js';
import './application/invitations.js';





const showToast = (type, message) => {
    $(".app-alert-container").append(`
        <div class="alert alert-${type} alert-dismissible" role="alert">
            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>
                ${message}
        </div>
    `)
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');


$(".confirm-invitation").on("click", function () {
    let id = $(this).attr('id');
    console.log(id);
    console.log(csrftoken);
    $.ajax({
        method: 'POST',
        url: "invitations/confirm-invitation",
        headers: {
            'X-CSRFToken': csrftoken
        },
        data: {
            id: id
        }
    })
        .done(function (response) {
            showToast('success', response.message);
            $(`#invitationId${id}`).remove();
        })
        .fail(function (response) {
            console.log(response);
        });
});

$(".cancel-invitation").on("click", function () {
    let id = $(this).attr('id');
    console.log(id);
    console.log(csrftoken);
    $.ajax({
        method: 'POST',
        url: "invitations/cancel-invitation",
        headers: {
            'X-CSRFToken': csrftoken
        },
        data: {
            id: id
        }
    })
        .done(function (response) {
            showToast('success', response.message);
            $(`#invitationId${id}`).remove();
        })
        .fail(function (response) {
            console.log(response);
        });
});
const showToast = (type, message) => {
    $(".app-alert-container").append(`
        <div class="alert alert-${type} alert-dismissible" role="alert">
            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>
                ${message}
        </div>
    `)
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');


$(".invite-player-button").on("click", function () {
    let id = $(this).attr('id');
    console.log(id);
    console.log(csrftoken);
    $.ajax({
        method: 'POST',
        url: "invite-player",
        headers: {
            'X-CSRFToken': csrftoken
        },
        data: {
            id: id
        }
    })
        .done(function (response) {
            showToast('success', response.message);
            $(`#playerStatisticsId${id}`).remove();
        })
        .fail(function (response) {
            console.log(response);
        });
});