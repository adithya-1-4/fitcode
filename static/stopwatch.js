// Stopwatch functionality
// Define variables to hold time values
let seconds = 0;
let minutes = 0;
let hours = 0;

// Define vars to hold display values
let displaySeconds = 0;
let displayMinutes = 0;
let displayHours = 0;

// Define var to hold interval function
let interval = null;

// Define var to hold stopwatch status
let status = "stopped";

// Initialize stopwatch
document.addEventListener('DOMContentLoaded', function() {
    // Check if elements exist to avoid errors
    if (document.getElementById("startStop") && document.getElementById("display")) {
        document.getElementById("startStop").addEventListener("click", startStop);
        
        if (document.getElementById("reset")) {
            document.getElementById("reset").addEventListener("click", reset);
        }
    }
});

// Stopwatch function (logic to determine when to increment next value etc.)
function stopwatch() {
    seconds++;

    // Logic to determine when to increment next value
    if (seconds / 60 === 1) {
        seconds = 0;
        minutes++;

        if (minutes / 60 === 1) {
            minutes = 0;
            hours++;
        }
    }

    // Format display values
    displaySeconds = seconds < 10 ? "0" + seconds : seconds;
    displayMinutes = minutes < 10 ? "0" + minutes : minutes;
    displayHours = hours < 10 ? "0" + hours : hours;

    // Display updated time values to user
    document.getElementById("display").innerHTML = displayHours + ":" + displayMinutes + ":" + displaySeconds;
}

// Function to start/stop the stopwatch
function startStop() {
    if (status === "stopped") {
        // Start the stopwatch by calling the setInterval function
        interval = window.setInterval(stopwatch, 1000);
        status = "started";
        document.getElementById("startStop").innerHTML = "Stop";
        document.getElementById("startStop").className = "btn btn-outline-danger btn-lg";
    } else {
        // Stop the stopwatch
        window.clearInterval(interval);
        document.getElementById("startStop").innerHTML = "Start";
        document.getElementById("startStop").className = "btn btn-outline-success btn-lg";
        status = "stopped";
    }
}

// Function to reset the stopwatch
function reset() {
    window.clearInterval(interval);
    
    // Reset time values
    seconds = 0;
    minutes = 0;
    hours = 0;
    
    // Reset display values
    document.getElementById("display").innerHTML = "00:00:00";
    document.getElementById("startStop").innerHTML = "Start";
    document.getElementById("startStop").className = "btn btn-outline-success btn-lg";
    status = "stopped";
}