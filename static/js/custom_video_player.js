(async function ($) {
    //Get Elements
    var selectVideo = document.querySelector('video');
    var playButton = document.querySelector('.toggle');
    var inputItem = document.querySelectorAll('input');
    var skipButton = document.querySelectorAll('.player__button[data-skip]');
    var progressBarOut = document.querySelector('.progress');
    var progressBarIn = document.querySelector('.progress__filled');
    // 全螢幕
    const fullScreen = document.querySelector('.full__screen');

    selectVideo.currentTime = 0;

    // Add EventListener
    playButton.addEventListener('click', playToggle);
    selectVideo.addEventListener('click', playToggle);
    // volumeSlide.addEventListener('input', changeVolume);
    // rateSlide.addEventListener('input', changeRate);
    inputItem.forEach(function (item) {
        item.addEventListener('input', changeCondition);
    });

    skipButton.forEach(function (button) {
        button.addEventListener('click', skipVideo)
    });
    selectVideo.addEventListener('timeupdate', progressing);
    progressBarOut.addEventListener('mousedown', addDragProgress);
    progressBarOut.addEventListener('mouseup', removeDragProgress);
    // 全螢幕 start
    fullScreen.addEventListener('click', goFullScreen);
    // 全螢幕 end

    //Create Functions
    function playToggle() {
        if (selectVideo.paused) {
            selectVideo.play();
            playButton.innerHTML = '❚ ❚';
            console.log(selectVideo.paused);
        } else {
            selectVideo.pause();
            playButton.innerHTML = '►';
            console.log(selectVideo.paused);
        }
    };

    function changeCondition(event) {
        let changeInput = event.target;
        let conditionName = changeInput.name;
        let conditionValue = changeInput.value;
        selectVideo[conditionName] = conditionValue;
    };


    function skipVideo(event) {
        let changeTime = parseInt(event.target.dataset.skip);
        selectVideo.currentTime += changeTime;
    };

    function progressing() {
        let videoDuration = selectVideo.duration;
        let currentPosition = selectVideo.currentTime;
        currentProgress = currentPosition / videoDuration * 100;
        progressBarIn.style.flexBasis = `${currentProgress}%`;
    };

    function addDragProgress(e) {
        progressBarOut.addEventListener('mousedown', dragProgressBar);
        progressBarOut.addEventListener('mousemove', dragProgressBar);
    };

    function removeDragProgress() {
        progressBarOut.removeEventListener('mousemove', dragProgressBar);
    };

    async function dragProgressBar(e) {
        let videoDuration = selectVideo.duration;
        let mouseX = e.offsetX;
        let progressBarWidth = progressBarOut.offsetWidth;
        let videoProgress = mouseX / progressBarWidth;
        let newPosition = videoDuration * videoProgress;

        selectVideo.currentTime = newPosition;
    };
    // 全螢幕 start
    function goFullScreen() {
        var requestMethod = selectVideo.requestFullScreen || selectVideo.webkitRequestFullScreen || selectVideo.mozRequestFullScreen || selectVideo.msRequestFullScreen;
        requestMethod.call(selectVideo);
    }
    // 全螢幕 end

    /*===========Add Keyboard Event===========*/
    window.addEventListener('keydown', keyboardFunction);

    function keyboardFunction(e) {
        e.preventDefault();

        if (e.keyCode === 37) {
            let backButton = document.querySelector('.player__button[data-skip="-10"]');
            console.log(backButton);
            backButton.click();
        };
        if (e.keyCode === 39) {
            let nextBotton = document.querySelector('.player__button[data-skip="25"]');
            console.log(nextBotton);
            nextBotton.click();

        };
        if (e.keyCode === 38 && selectVideo.volume <= 1) {
            let volumeSlide = document.querySelector('[name = "volume"]');
            volumeSlide.stepUp();
            selectVideo.volume = volumeSlide.value;
            console.log(volumeSlide.value);
        };
        if (e.keyCode === 40 && selectVideo.volume > 0) {
            let volumeSlide = document.querySelector('[name = "volume"]');
            volumeSlide.stepDown();
            selectVideo.volume = volumeSlide.value;

        };
        if (e.keyCode === 32) {
            playToggle();
        };
    };
    // 關閉 boostrap light box 的時候會暫停影片
    $('#exampleModal').on('hidden.bs.modal', function () {
        selectVideo.pause();
    })
})(jQuery);