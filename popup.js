let mediaRecorder;
let audioChunks = [];

document.getElementById('startRecordingBtn').addEventListener('click', startRecording);
document.getElementById('stopRecordingBtn').addEventListener('click', stopRecording);

async function startRecording() {
    try {
        // Request access to the microphone
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

        mediaRecorder = new MediaRecorder(stream);

        mediaRecorder.ondataavailable = event => {
            audioChunks.push(event.data);
        };

        mediaRecorder.onstop = () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            audioChunks = [];  // Clear audio chunks
            uploadAudio(audioBlob);
        };

        mediaRecorder.start();
        console.log("Recording started...");

        // Add "recording" class to change the button color to blue
        const startButton = document.getElementById('startRecordingBtn');
        startButton.classList.add('recording');  // Apply blue color
        startButton.classList.remove('stopped');  // Ensure it's green when stopped
        startButton.innerText = 'Recording...';

        // Toggle buttons for user interaction
        startButton.style.display = 'none'; // Hide the start button
        document.getElementById('stopRecordingBtn').style.display = 'block'; // Show stop button
    } catch (error) {
        console.error("Error accessing microphone:", error);
        alert("Please allow microphone access!");
    }
}

function stopRecording() {
    mediaRecorder.stop();
    console.log("Recording stopped.");

    // Add "stopped" class to change the button color back to green
    const startButton = document.getElementById('startRecordingBtn');
    startButton.classList.add('stopped');  // Apply green color
    startButton.classList.remove('recording');  // Remove blue color
    startButton.innerText = 'Start Recording';

    // Toggle buttons for user interaction
    startButton.style.display = 'block'; // Show the start button again
    document.getElementById('stopRecordingBtn').style.display = 'none'; // Hide stop button
}

function uploadAudio(audioBlob) {
    const formData = new FormData();
    formData.append("audio", audioBlob, "audio.wav");

    // Send audio data to server
    fetch('http://127.0.0.1:5000/upload_audio', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        if (data.transcription) {
            document.getElementById('result').innerText = "Transcription: " + data.transcription;
        } else {
            document.getElementById('result').innerText = "Error: " + data.error;
        }
    })
    .catch(error => {
        console.error('Error uploading audio:', error);
    });
}