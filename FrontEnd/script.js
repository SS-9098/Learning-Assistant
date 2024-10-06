// Handle sending a question via the input
let CurPro="default";
document.getElementById("submit-btn").addEventListener("click", function() {
    let question = document.getElementById("input").value;
    if (question) {
        // Display the user's question in the output area (for demo purposes)
        document.getElementById("output").innerText = "Processing: " + question;
        if(CurPro != "default"){
            fetch("http://127.0.0.1:5000/pq_update", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ name: CurPro, ques: question })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                } else {
                    document.getElementById("history-2").innerText = data.pq1
                    document.getElementById("history-1").innerText = question
                }
            })
            .catch(error => {
                console.error('Error fetching user details:', error);
            });

        }
        else{
            document.getElementById("history-2").innerText = document.getElementById("history-1").innerText
            document.getElementById("history-1").innerText = question
        }
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
"work on this"
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
    document.getElementById("search-1").innerText = "";
    document.getElementById("search-2").innerText = "";
    document.getElementById("partition").innerText = "";
});

// Handle profile selection
document.getElementById("shlok-profile").addEventListener("click", function() {
    alert("Switched to profile: Shlok Mishra");
    document.getElementById("profile").innerText = "Shlok Mishra";
    CurPro= "Shlok Mishra";
    document.getElementById("profile").innerText = "Shlok Mishra";
    document.getElementById("output").innerText = "";
    document.getElementById("answer").innerText = "";
    document.getElementById("input").value = "";
    document.getElementById("link").innerText = "";
    document.getElementById("search-1").innerText = "";
    document.getElementById("search-2").innerText = "";
    document.getElementById("partition").innerText = "";
    fetch('http://127.0.0.1:5000/get_user_details', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name: 'Shlok Mishra' })
    })
    .then(response => {
        if (!response.ok) {
            // If response is not ok, throw an error to the catch block
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            document.getElementById("history-2").innerText = data.pq2
            document.getElementById("history-1").innerText = data.pq1
        }
    })
    .catch(error => {
        console.error('Error fetching user details:', error);
    });
});

document.getElementById("daksh-profile").addEventListener("click", function() {
    alert("Switched to profile: Daksh Mohan");
    document.getElementById("profile").innerText = "Daksh Mohan";
    CurPro = "Daksh Mohan";
    document.getElementById("output").innerText = "";
    document.getElementById("answer").innerText = "";
    document.getElementById("input").value = "";
    document.getElementById("link").innerText = "";
    document.getElementById("search-1").innerText = "";
    document.getElementById("search-2").innerText = "";
    document.getElementById("partition").innerText = "";
    fetch('http://127.0.0.1:5000/get_user_details', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name: 'Daksh Mohan' })
    })
    .then(response => {
        if (!response.ok) {
            // If response is not ok, throw an error to the catch block
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            document.getElementById("history-2").innerText = data.pq2
            document.getElementById("history-1").innerText = data.pq1
        }
    })
    .catch(error => {
        console.error('Error fetching user details:', error);
    });
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
            if (data.title1) {
                // Display the answer in the output area
                document.getElementById("search-1").innerText = data.title1;
                document.getElementById("search-1").href = data.link1;
                document.getElementById("partition").innerText = "\u00A0\u00A0||\u00A0\u00A0";
                document.getElementById("search-2").innerText = data.title2;
                document.getElementById("search-2").href = data.link2;
            } else if (data.error) {
                // Display an error message if the backend returns an error
                document.getElementById("search-1").innerText = "Error: " + data.error;
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
// Function to fetch user details from the server
/*function fetchUserDetails(name) {
    fetch('http://127.0.0.1:5000/get_user_details', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name: name })
    })
    .then(response => {
        if (!response.ok) {
            // If response is not ok, throw an error to the catch block
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            updateDashboard(data);
        }
    })
    .catch(error => {
        console.error('Error fetching user details:', error);
    });
}

// Function to update the dashboard with user details
function updateDashboard(user) {
    document.querySelector(".left-dashboard").innerHTML = `
        <h2>${user.name}</h2>
        <p>Email: ${user.email}</p>
        <p>Profession: ${user.profession}</p>
    `;
}

// Handle profile selection for Shlok Mishra
document.getElementById("shlok-profile").addEventListener("click", function() {
    fetchUserDetails("Shlok Mishra");
});

// Handle profile selection for Daksh Mohan
document.getElementById("daksh-profile").addEventListener("click", function() {
    fetchUserDetails("Daksh Mohan");
});
*/

