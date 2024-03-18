document.addEventListener('DOMContentLoaded', function () {
    var links = document.querySelectorAll('#menu a, #paginations a, #title a, #genre a, .playlists a');
    
    links.forEach(function (link) {
        link.addEventListener('click', handleLinkClick);
    });

   
});

function handleLinkClick(event) {
    event.preventDefault();
    let songPage = false;
    var url = event.target.href;
    if (url.match(/uploaded_by/))
    songPage = true;
    $.ajax({
        url: url,
        method: 'GET',
        headers: { 'X-Requested-With': 'XMLHttpRequest' },
        dataType: 'json',
        success: function (data) {
            updateContent(data, songPage);
            updateUrl(url);
            initAudioPlayer();
            initializeModals();
            var newLinks = document.querySelectorAll('#paginations a, #title a');
            newLinks.forEach(function (link) {
                link.addEventListener('click', handleLinkClick);
            });
        },
        error: function (error) {
            console.error('Error:', error);
        },
    });
}


function updateContent(data, songPage) {
    $('.cover_play_pagin').html(data.songs);
    if (songPage)
        $(".songPage").html(data.song);
    else
        $(".songPage").remove()

}
function updateUrl(url) {
        window.history.pushState({ path: url }, '', url);
    }