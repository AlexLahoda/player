document.addEventListener('DOMContentLoaded', function () {
    initAudioPlayer();
});

function initAudioPlayer() {
    let savedTime;
    let updPlTime;
    var currentIndex = 0; 
    var playlist = []; 
    let outPlayer = document.getElementById('outPlayer');
    
    const items = document.querySelectorAll(".item");
    const src = items[0].src.split('/');
    const end = src.length-1;

    let playImage = src.slice(0,end) ;
    playImage.push('play.png');
    playImage = playImage.join('/');
    let pauseImage = src.slice(0,end);
    pauseImage.push('stop.png');
    pauseImage = pauseImage.join('/');

    items.forEach(item =>{

        outPlayer.addEventListener("play", function() {
            if ($(item).data('url').split('/').pop() == outPlayer.src.split('/').pop())
                item.src = pauseImage;
            else
                item.src = playImage;
        });
    
        outPlayer.addEventListener("pause", function() {
            if ($(item).data('url').split('/').pop() == outPlayer.src.split('/').pop()){
                item.src = playImage;
        }
        });
        outPlayer.addEventListener("ended", function() {
            if ($(item).data('url').split('/').pop() == outPlayer.src.split('/').pop()){
            item.src = playImage;
        }
        });
    });

    $('#prevBtn').on('click', function() {
        currentIndex = (currentIndex - 1 + playlist.length) % playlist.length;
        playAudio();
    });
    $('#nextBtn').on('click', function() {
        currentIndex = (currentIndex + 1) % playlist.length;
        playAudio();
    });

    $('img.item').click(function() {
        currentIndex = $('.item').index(this);

        playlist = $('.item').map(function() {
            return $(this).data('url');
        }).get();
        playAudio();
    });
    $('#outPlayer').on('ended', function() {
        currentIndex = (currentIndex + 1) % playlist.length;
        playAudio();
    });
    
    function setupPlaylist(audioUrl) {
        outPlayer.src = audioUrl;
    }
    
    function playAudio() {
        var AudioId = $(`#toplay img.item:eq(${currentIndex})`).attr('id');
        let prev = outPlayer.src;
        let isPaused = outPlayer.paused
        savedTime = outPlayer.currentTime;
        setupPlaylist(playlist[currentIndex]);
        let now = outPlayer.src;
        if (prev == now && !isPaused){
            outPlayer.pause();
            updPlTime = savedTime;
            items.forEach(item =>{
                if ($(item).data('url').split('/').pop() == outPlayer.src.split('/').pop()){
                    item.src = playImage;
            }
            });
        }
        else if(prev == now && isPaused){
            increaseListenCount(AudioId);
            outPlayer.currentTime = updPlTime;
            outPlayer.play();
            }
        else{
            increaseListenCount(AudioId);
            outPlayer.play();
        }
    }
}

function increaseListenCount(audioId) {
    let csrf = $('input[name="csrfmiddlewaretoken"]').val();
    let action = 'count';
    $.ajax({
        url: `/reaction_counter/`,
        method: 'POST',
        data: {
            "csrfmiddlewaretoken": csrf,
            "song_id": audioId,
            "action": action,
        },
        success: function(response) {
            let spanId = `counterId${audioId}`
            let span = document.getElementById(spanId)
            span.innerText = response.counter
        },
    });
}


