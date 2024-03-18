$(document).ready(function () {
    $('.likeButton').click(function () {
        let csrf = $('input[name="csrfmiddlewaretoken"]').val();
        let img = $(this);
        let action;
        src = img.attr('src').split('/');
        end = src.length-1
        // alert(src[end]);
        // src.push(src[end]);
        // src = src.join('/');
        // alert(src);
        if (src[end]=="Like.png")
            action = 'add';
        else
            action = 'remove';
        $.ajax({
            url: '/reaction_counter/',
            type: 'POST',
            data: {
                "csrfmiddlewaretoken": csrf,
                "song_id": $(this).attr('id'),
                "action": action,
            },
            success: function (data) {
                if (action=='add'){
                    src.splice(end,1,'Liked.png')
                    src = src.join('/');
                    img.attr('src', src);
                }
                else
                    src.splice(end,1,'Like.png')
                    src = src.join('/');
                    img.attr('src', src);
            }
        })
    })

    $('.delButton').click(function () {
        let csrf = $('input[name="csrfmiddlewaretoken"]').val();
        let img = $(this);
        let song_id = $(this).attr('id')
        result = confirm('Ви дійсно хочете видалити цю композицію?');
        if (result){
        let action='del';
        $.ajax({
            url: '/reaction_counter/',
            type: 'POST',
            data: {
                "csrfmiddlewaretoken": csrf,
                "song_id": song_id,
                "action": action,
            },
            success: function (data) {
                document.getElementById(`li${song_id}`).remove();
            }
        })
    }
    })

    $('.del_pl').click(function () {
        let csrf = $('input[name="csrfmiddlewaretoken"]').val();
        let songId = this.getAttribute("data-songid");
        const currentUrl = window.location.href;
        $.ajax({
            url: '/add_to_pl/',
            type: 'POST',
            data: {
                "csrfmiddlewaretoken": csrf,
                "song_id": songId,
                "action": 'del_pl',
                'path': currentUrl,
            },
            success: function (data) {
                document.getElementById(`li${songId}`).remove();
            }
        })
    })
})
