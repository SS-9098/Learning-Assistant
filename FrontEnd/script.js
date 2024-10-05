// Handle sending a question via the input
document.getElementById("submit-btn").addEventListener("click", function() {
    let question = document.getElementById("input").value;
    if (question) {
        // Display the user's question in the output area (for demo purposes)
        document.getElementById("output").innerText = "Processing: " + question;

        // Here you would normally send the question to the API, e.g., using fetch or axios
        // Then display the API response in the output area.
    }
});

// Voice button - For demo, it will print "Listening..."
document.getElementById("voice-btn").addEventListener("click", function() {
    document.getElementById("output").innerText = "Listening...";
    
    // You can integrate a speech recognition API here (like Web Speech API)
});

// Enable Speech-to-Text with double-tab press
document.addEventListener("keydown", function(event) {
    if (event.key === "Tab") {
        let doubleTabTimeout = null;
        if (!doubleTabTimeout) {
            doubleTabTimeout = setTimeout(function() {
                doubleTabTimeout = null; // Reset double tab detection
            }, 300); // 300ms for double tab
        } else {
            document.getElementById("output").innerText = "Speech-to-Text Activated!";
            clearTimeout(doubleTabTimeout);
            doubleTabTimeout = null; // Reset for next double tab
        }
    }
});

// New conversation button logic
document.getElementById("new-conversation").addEventListener("click", function() {
    document.getElementById("output").innerText = "Starting a new conversation...";
    document.getElementById("input").value = "";
});

// Continue learning logic
document.getElementById("continue-learning").addEventListener("click", function() {
    document.getElementById("output").innerText = "Continuing with your learning materials...";
});
document.getElementById("submit-btn").addEventListener("click", function () {
    let question = document.getElementById("input").value;
    
    if (question) {
        // Display the user's question in the output area
        document.getElementById("output").innerText = "Processing: " + question;

        // Send the question to the Flask backend
        fetch("http://127.0.0.1:5000/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ question: question })
        })
        .then(response => response.json())
        .then(data => {
            if (data.answer) {
                // Display the answer in the output area
                document.getElementById("answer").innerText = data.answer;
            } else if (data.error) {
                // Display an error message if the backend returns an error
                document.getElementById("answer").innerText = "Error: " + data.error;
            }
        })
        .catch(error => {
            // Handle any network errors
            document.getElementById("output").innerText = "Error: " + error.message;
        });
    }
});

// Check if the browser supports speech recognition
window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

// Create a new speech recognition object once when the script runs
let recognition;

if ('SpeechRecognition' in window) {
    recognition = new window.SpeechRecognition();
    recognition.continuous = true;  // Keep listening even after speech is recognized
    recognition.interimResults = false; // Get only final results
    recognition.lang = 'en-US'; // Set the language for recognition

    // When recognition starts
    recognition.onstart = function() {
        document.getElementById("output").innerText = "Listening...";
    };

    // When speech is recognized
    recognition.onresult = function(event) {
        const speechResult = event.results[0][0].transcript;
        document.getElementById("input").value = speechResult; // Display recognized speech in the input field
        document.getElementById("output").innerText = "You said: " + speechResult;
    };

    // Handle recognition errors
    recognition.onerror = function(event) {
        document.getElementById("output").innerText = "Error: " + event.error;
    };

    // When recognition ends
    recognition.onend = function() {
        document.getElementById("output").innerText = "Speech recognition stopped.";
    };

} else {
    document.getElementById("output").innerText = "Speech recognition is not supported in this browser.";
}

// Add event listener for the voice button
document.getElementById("voice-btn").addEventListener("click", function () {
    if (recognition) {
        recognition.start();  // Start listening for speech
    }
});

