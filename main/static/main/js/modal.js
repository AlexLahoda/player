document.addEventListener('DOMContentLoaded', function () {
    initializeModals()
});

function initializeModals() {
    let csrf = $('input[name="csrfmiddlewaretoken"]').val();
    const modal = document.getElementById("myModal");
    const openModalButtons = document.querySelectorAll(".openModalBtn");
    const closeModalBtn = document.getElementById("closeModalBtn");
    const submitBtn = document.getElementById("submitBtn");
    
    openModalButtons.forEach(button => {
        button.addEventListener("click", function () {
            const songId = this.getAttribute("data-songid");
            modal.setAttribute("data-songid", songId);
            modal.style.display = "block";
        });
    });

    closeModalBtn.addEventListener("click", function () {
        modal.style.display = "none";
    });

    submitBtn.addEventListener("click", function () {
        const songId = modal.getAttribute("data-songid");
        const selectedPlaylists = [];
        const playlistCheckboxes = document.getElementsByName("playlist");

        playlistCheckboxes.forEach(checkbox => {
            if (checkbox.checked) {
                selectedPlaylists.push(checkbox.value);
            }
        });
        console.log(selectedPlaylists);

        $.ajax({
            url: '/add_to_pl/',
            type: 'POST',
            data: {
                "csrfmiddlewaretoken": csrf,
                "song_id": songId,
                "playlists":JSON.stringify(selectedPlaylists),
                'action': 'add_pl',
            },
            success: function (data) {
              
            }
        })

        modal.style.display = "none";
    });
}
