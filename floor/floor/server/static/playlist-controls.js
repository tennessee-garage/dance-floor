var refreshHandle;
var bpmSamples = [];
var bpmAbortTimeoutHandle;
var lastStatus = null;

function handleShowStart() {
    console.log('Playlist started');

    var startButton = document.getElementById('start-button');
    var stopButton = document.getElementById('stop-button');

    startButton.style.display = 'none';
    stopButton.style.display = 'block';
}

function handleShowStop() {
    console.log('Playlist stopped');

    var startButton = document.getElementById('start-button');
    var stopButton = document.getElementById('stop-button');

    startButton.style.display = 'block';
    stopButton.style.display = 'none';
}

function handlePlaylistUpdate(playlist) {
    console.log('Playlist:', playlist);

    var playlistDiv = document.getElementById('playlist');
    var listGroup = document.createElement('ul');
    var time_indicator = '';
    listGroup.className = 'list-group';

    var activeElement = null;
    for (var i = 0; i < playlist.queue.length; i++) {
        var playlistItem = document.createElement('a');
        var isActive = (i === playlist.current_position);

        if (isActive) {
            activeElement = playlistItem;
            playlistItem.className = 'list-group-item list-group-item-success';

            var seconds_remaining = parseInt(playlist.millis_remaining/1000);
            time_indicator = ' <i>(Time Remaining: ' + seconds_remaining + 's)</i>';
        } else {
            playlistItem.className = 'list-group-item';
            time_indicator = '';
        }

        var seconds_remaining = parseInt(playlist.millis_remaining/1000)
        playlistItem.innerHTML = '' + (i+1) + '. ' + playlist.queue[i].name + time_indicator;
        listGroup.appendChild(playlistItem);
    }

    playlistDiv.innerHTML = '';
    playlistDiv.appendChild(listGroup);

    if (activeElement) {
        activeElement.scrollIntoView();
    }
}

function getStatus() {
    return axios.get('/api/status').then(function (response) {
        handlePlaylistUpdate(response.data.playlist);
        handleTempoUpdate(response.data.tempo);
        handleBrightnessUpdate(response.data.brightness);
        handleLayersUpdate(response.data.layers, response.data.processors);
        rescheduleRefresh();
        lastStatus = response.data;
    }).catch(function (error) {
        handleError(error);
        rescheduleRefresh();
    });
}

function start_show() {
    return axios.post('/api/playlist/start').then(function (response) {
        handleShowStart(response.data);
        rescheduleRefresh();
    }).catch(function (error) {
        handleError(error);
        rescheduleRefresh();
    });
}

function stop_show() {
    return axios.post('/api/playlist/stop').then(function (response) {
        handleShowStop(response.data);
        rescheduleRefresh();
    }).catch(function (error) {
        handleError(error);
        rescheduleRefresh();
    });
}

function advance() {
    return axios.post('/api/playlist/advance').then(function (response) {
        handlePlaylistUpdate(response.data);
        rescheduleRefresh();
    }).catch(function (error) {
        handleError(error);
        rescheduleRefresh();
    });
}

function previous() {
    return axios.post('/api/playlist/previous').then(function (response) {
        handlePlaylistUpdate(response.data);
        rescheduleRefresh();
    }).catch(function (error) {
        handleError(error);
        rescheduleRefresh();
    });
}

function stay() {
    return axios.post('/api/playlist/stay').then(function (response) {
        handlePlaylistUpdate(response.data);
        rescheduleRefresh();
    }).catch(function (error) {
        handleError(error);
        rescheduleRefresh();
    });
}

function setTempo(bpm) {
    var data = {
        bpm: bpm,
    };
    console.log('Setting tempo to: ', data);
    return axios.post('/api/tempo', data).then(function (response) {
        handleTempoUpdate(response.data);
    }).catch(function (error) {
        handleError(error);
    });
}

function nudgeTempo(bpmDelta, downbeatMillisDelta) {
    var data = {
        bpm_delta: bpmDelta,
        downbeat_millis_delta: downbeatMillisDelta,
    };
    console.log('Nudging tempo by: ', data);
    return axios.post('/api/tempo/nudge', data).then(function (response) {
        handleTempoUpdate(response.data);
    }).catch(function (error) {
        handleError(error);
    });
}

function handleTempoUpdate(tempoData) {
    var status = document.getElementById('bpm');
    status.value = tempoData.bpm;
}

function setLayer(layerName, processorName) {
    var data = {
        processor_name: processorName,
    };
    return axios.patch('/api/layers/' + layerName, data).then(function (response) {
        return getStatus();
    }).catch(function (error) {
        handleError(error);
    });
}

function hackyDeepEqual(a, b) {
    return JSON.stringify(a) === JSON.stringify(b);
}

function handleLayersUpdate(layers, processors) {
    if (lastStatus && hackyDeepEqual(layers, lastStatus.layers)) {
        return;
    }

    Object.entries(layers).forEach(function (layerEntry) {
        var layerName = layerEntry[0];
        var layerDetail = layerEntry[1];
        var currentProcessor = layerDetail.processor_name;

        var layerSelect = document.createElement('select');
        layerSelect.className = 'form-control'
        layerSelect.id = layerName + '_select';

        var blank = document.createElement('option');
        blank.value = '';
        blank.text = '(inactive)';
        layerSelect.add(blank);

        Object.entries(processors).forEach(function (entry) {
            var processorName = entry[0];
            var option = document.createElement('option');
            option.value = processorName;
            option.text = processorName;
            layerSelect.add(option);
        });
        layerSelect.value = currentProcessor;

        var element = document.getElementById(layerName + '_controls');
        element.innerHTML = '';
        element.appendChild(layerSelect);

        layerSelect.addEventListener('change', function (e) {
            var newValue = e.target.value || '';
            setLayer(layerName, newValue);
        });
    });
}

function setBrightness(brightness) {
    var data = {
        brightness: brightness,
    };
    console.log('Setting brightness to: ', brightness);
    return axios.post('/api/brightness', data).then(function (response) {
        handleBrightnessUpdate(response.data.brightness);
    }).catch(function (error) {
        handleError(error);
    });
}

function handleBrightnessUpdate(brightnessValue) {
    var brightness = document.getElementById('brightness');
    var strValue = brightnessValue.toFixed(1);
    brightness.value = strValue;
}

function resetBpmTapper() {
    var tapper = document.getElementById('tapper');
    tapper.innerHTML = 'Tap BPM';
    bpmSamples = [];
}

function onBpmTapped() {
    var tapper = document.getElementById('tapper');
    var now = (new Date()).getTime();
    bpmSamples.push(now);

    // Clean things up if somone doesn't finish the job.
    if (bpmAbortTimeoutHandle) {
        clearTimeout(bpmAbortTimeoutHandle);
    }
    bpmAbortTimeoutHandle = setTimeout(resetBpmTapper, 5000);

    // Bail out early if we need more samples.
    if (bpmSamples.length < 4) {
        var remain = 4 - bpmSamples.length;
        tapper.innerHTML = 'Tap BPM (' + remain + ' more ...)';
        return;
    }

    if (bpmAbortTimeoutHandle) {
        clearTimeout(bpmAbortTimeoutHandle);
        bpmAbortTimeoutHandle = null;
    }

    // Compute and send BPM.
    var intervals = [
        bpmSamples[1] - bpmSamples[0],
        bpmSamples[2] - bpmSamples[1],
        bpmSamples[3] - bpmSamples[2]
    ];
    resetBpmTapper();

    var secondsPerBeat = (intervals[0] + intervals[1] + intervals[2]) / 3 / 1000;
    var beatsPerSecond = 1 / secondsPerBeat;
    var beatsPerMinute = beatsPerSecond * 60;
    beatsPerMinute = Math.round(beatsPerMinute * 10) / 10;

    if (beatsPerMinute < 60 || beatsPerMinute > 200) {
        console.error('Ignoring crazy BPM: ', beatsPerMinute);
        return;
    }

    setTempo(beatsPerMinute);
}

function onBpmNudgedLeft() {
    nudgeTempo(-0.1);
}

function onBpmNudgedRight() {
    nudgeTempo(0.1);
}

function onDownbeatNudgedLeft() {
    nudgeTempo(null, -100);
}

function onDownbeatNudgedRight() {
    nudgeTempo(null, 100);
}

function onBrightnessChanged(e) {
    var value = e.target.value
    setBrightness(value);
}

function installListeners() {
    $('#start-button').click(function () {
        start_show();
    });
    $('#stop-button').click(function () {
        stop_show();
    });
    $('#previous-button').click(function () {
        previous();
    });
    $('#next-button').click(function () {
        advance();
    });
    $('#stay-button').click(function () {
        stay();
    });
    $('#tapper').click(function () {
        onBpmTapped();
    });
    $('#bpm-nudge-left').click(function () {
        onBpmNudgedLeft();
    });
    $('#bpm-nudge-right').click(function () {
        onBpmNudgedRight();
    });
    $('#downbeat-nudge-left').click(function () {
        onDownbeatNudgedLeft();
    });
    $('#downbeat-nudge-right').click(function () {
        onDownbeatNudgedRight();
    });
    $('#brightness').change(function (e) {
        onBrightnessChanged(e);
    });
}

function rescheduleRefresh() {
    if (refreshHandle) {
        clearTimeout(refreshHandle);
    }
    refreshHandle = setTimeout(getStatus, 2000);
}

getStatus();
installListeners();