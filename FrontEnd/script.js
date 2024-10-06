// Handle sending a question via the input
document.getElementById("submit-btn").addEventListener("click", function() {
    let question = document.getElementById("input").value;
    if (question) {
        // Display the user's question in the output area (for demo purposes)
        document.getElementById("output").innerText = "Processing: " + question;
        document.getElementById("history-2").innerText = document.getElementById("history-1").innerText
        document.getElementById("history-1").innerText = question
        // Here you would normally send the question to the API, e.g., using fetch or axios
        // Then display the API response in the output area.
    }
});

document.getElementById("history-1").addEventListener("click", function() {
    document.getElementById("input").value = document.getElementById("history-1").innerText;
});
document.getElementById("history-2").addEventListener("click", function() {
    document.getElementById("input").value = document.getElementById("history-2").innerText;
});
// Voice button - For demo, it will print "Listening..."
document.getElementById("voice-btn").addEventListener("click", function() {

    
    // You can integrate a speech recognition API here (like Web Speech API)
    fetch("http://127.0.0.1:5000/voice", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
        })
        .then(document.getElementById("output").innerText = "Listening...")
        .then(response => response.json())
        .then(data => {
            if (data.speech) {
                // Display the answer in the output area
                document.getElementById("output").innerText = "";
                document.getElementById("input").value = data.speech;
            } else if (data.error) {
                // Display an error message if the backend returns an error
                document.getElementById("output").innerText = "Error: " + data.error;
            }
        })
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
    document.getElementById("output").innerText = "";
    document.getElementById("answer").innerText = "";
    document.getElementById("input").value = "";
    document.getElementById("link").innerText = "";
    document.getElementById("search").innerText = "";
});

// Handle profile selection
document.getElementById("shlok-profile").addEventListener("click", function() {
    alert("Switched to profile: Shlok Mishra");
    // Add your logic here for handling Shlok's profile
});

document.getElementById("daksh-profile").addEventListener("click", function() {
    alert("Switched to profile: Daksh Mohan");
    // Add your logic here for handling Daksh's profile
});
// Toggle profile dropdown visibility on click
document.querySelector(".dropbtn-profile").addEventListener("click", function() {
    const dropdown = document.querySelector(".dropdown-content-profile");
    // Toggle the display between 'none' and 'block'
    if (dropdown.style.display === "block") {
        dropdown.style.display = "none";
    } else {
        dropdown.style.display = "block";
    }
});

// Close the dropdown if clicked outside of it
window.addEventListener("click", function(event) {
    if (!event.target.matches('.dropbtn-profile')) {
        const dropdown = document.querySelector(".dropdown-content-profile");
        if (dropdown.style.display === "block") {
            dropdown.style.display = "none";
        }
    }
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
            body: JSON.stringify({ question: question + "within 100 words" })
        })
        .then(response => response.json())
        .then(data => {
            if (data.answer) {
                // Display the answer in the output area
                document.getElementById("answer").innerText = data.answer;
                document.getElementById("output").innerText = question;
                document.getElementById("input").value = "";
            } else if (data.error) {
                // Display an error message if the backend returns an error
                document.getElementById("answer").innerText = "Error: " + data.error;
            }
        })
        .catch(error => {
            // Handle any network errors
            document.getElementById("output").innerText = "Error: " + error.message;
        });

        //Get video link and name
        fetch("http://127.0.0.1:5000/video", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ question: question })
        })
        .then(response => response.json())
        .then(data => {
            if (data.name) {
                // Display the answer in the output area
                document.getElementById("link").innerText = " " + data.name;
                document.getElementById("link").href = data.link;
            } else if (data.error) {
                // Display an error message if the backend returns an error
                document.getElementById("video").innerText = "Error: " + data.error;
            }
        })
        .catch(error => {
            // Handle any network errors
            document.getElementById("output").innerText = "Error: " + error.message;
        });
        //Fetch article title and link
        fetch("http://127.0.0.1:5000/search", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ question: question })
        })
        .then(response => response.json())
        .then(data => {
            if (data.title) {
                // Display the answer in the output area
                document.getElementById("search").innerText = " " + data.title;
                document.getElementById("search").href = data.link;
            } else if (data.error) {
                // Display an error message if the backend returns an error
                document.getElementById("search").innerText = "Error: " + data.error;
            }
        })
        .catch(error => {
            // Handle any network errors
            document.getElementById("output").innerText = "Error: " + error.message;
        });
    }
});

// Check if the browser supports speech recognition

// Add event listener for the voice button
document.getElementById("voice-btn").addEventListener("click", function () {
    if (recognition) {
        recognition.start();  // Start listening for speech
    }
});

