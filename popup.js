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

        // Toggle buttons for user
        document.getElementById('startRecordingBtn').style.display = 'none';
        document.getElementById('stopRecordingBtn').style.display = 'block';
    } catch (error) {
        console.error("Error accessing microphone:", error);
        alert("Please allow microphone access!");
    }
}

function stopRecording() {
    mediaRecorder.stop();
    console.log("Recording stopped.");

    // Toggle buttons for user
    document.getElementById('startRecordingBtn').style.display = 'block';
    document.getElementById('stopRecordingBtn').style.display = 'none';
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
