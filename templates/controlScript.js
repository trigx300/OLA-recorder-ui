let isCurrentlyPlaying = false; // Global state to track playback

document.addEventListener('DOMContentLoaded', function() {
    initializeUI();
    attachEventListeners();
});

function initializeUI() {
    updateRecordingsList();
    // Additional UI setup can be added here
}

function attachEventListeners() {
    document.getElementById('recordButton').addEventListener('click', handleRecord);
    document.getElementById('togglePlaybackButton').addEventListener('click', function() {
        togglePlayback(this);
    });
    document.getElementById('renameButton').addEventListener('click', renameFile);
    document.getElementById('deleteButton').addEventListener('click', deleteFile);
    document.getElementById('broadcastButton').addEventListener("click", toggleBroadcast);
}

function updateRecordingsList() {
    fetch('/list_art_files')
        .then(response => response.json())
        .then(data => {
            const playbackSelection = document.getElementById('playbackSelection');
            playbackSelection.innerHTML = ''; // Clear existing options
            data.files.forEach(file => {
                const option = document.createElement('option');
                option.value = file;
                option.textContent = file;
                playbackSelection.appendChild(option);
            });
        })
        .catch(error => console.error('Error fetching recordings:', error));
}

function handleRecord() {
    const button = document.getElementById('recordButton');
    const isRecording = button.classList.contains('recording');
    const action = isRecording ? 'stop' : 'start';
    const filenameInput = document.getElementById('filenameInput');
    const filename = filenameInput.value.trim();
    const universe = document.getElementById('universeSelection').value;

    if (action === 'start' && !filename) {
        showFeedback('Please enter a filename.', 'danger');
        return;
    }

    fetch('/record', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action, filename, universe })
    })
    .then(response => response.json())
    .then(data => {
        showFeedback(data.message, 'success');
        button.textContent = isRecording ? 'Start Recording' : 'Stop Recording';
        button.classList.toggle('recording', !isRecording);
        updateRecordingsList();
        if (action === 'start') filenameInput.value = ''; // Clear filename input after starting
    })
    .catch(error => {
        console.error('Error:', error);
        showFeedback('An error occurred.', 'danger');
    });
}

function togglePlayback(button) {
    const action = isCurrentlyPlaying ? 'stop' : 'start';
    const filename = document.getElementById('playbackSelection').value;

    fetch('/play', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: action, filename: filename })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok.');
        }
        return response.json();
    })
    .then(data => {
        isCurrentlyPlaying = !isCurrentlyPlaying;
        button.textContent = isCurrentlyPlaying ? 'Stop' : 'Play';
        button.classList.toggle('playing', isCurrentlyPlaying);
        showFeedback(data.message, 'success');
    })
    .catch(error => {
        console.error('Error:', error);
        showFeedback('Failed to toggle playback. ' + error.message, 'danger');
    });
}

function renameFile() {
    // Your existing rename implementation
}

function deleteFile() {
    // Your existing delete implementation
}

function toggleBroadcast() {
    // Assuming you have an implementation for broadcasting toggle
}

function showFeedback(message, type) {
    const feedbackAlert = document.getElementById('feedbackAlert');
    feedbackAlert.textContent = message;
    feedbackAlert.className = `alert alert-${type}`;
    feedbackAlert.style.display = 'block';
    setTimeout(() => { feedbackAlert.style.display = 'none'; }, 3000);
}
