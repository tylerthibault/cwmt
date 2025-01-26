
document.addEventListener('DOMContentLoaded', function () {
    var allProgressBars = document.querySelectorAll('#flash-progress');
    allProgressBars.forEach(function (progressBar) {
        update_progress(progressBar);
    });
});

function update_progress(progressBar) {
    var width = 100;
    var timeRemaining = 10; // Time in seconds
    var interval = setInterval(function () {
        if (timeRemaining <= 0) {
            clearInterval(interval);
            var flashBox = progressBar.closest('.flash_box');
            if (flashBox) {
                flashBox.style.display = 'none';
            }
        } else {
            timeRemaining--;
            width = (timeRemaining / 10) * 100;
            progressBar.style.width = width + '%';
        }
    }, 1000);
    progressBar.dataset.intervalId = interval;
}

function close_flash() {
    var flashBox = event.target.closest('.flash_box');
    if (flashBox) {
        var progressBar = flashBox.querySelector('#flash-progress');
        if (progressBar && progressBar.dataset.intervalId) {
            clearInterval(Number(progressBar.dataset.intervalId));
        }
        flashBox.style.display = 'none';
    }
}

console.log('flash_messages.js loaded');
