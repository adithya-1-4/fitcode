// Timer functionality
// Define variables to hold time values
let tseconds = 0;
let tminutes = 0;
let thours = 0;

// Define vars to hold display values
let tdisplaySeconds = 0;
let tdisplayMinutes = 0;
let tdisplayHours = 0;

// Define var to hold interval function
let tinterval = null;

// Define var to hold timer status
let tstatus = "stopped";

// Initialize timer
document.addEventListener('DOMContentLoaded', function() {
    // Check if elements exist to avoid errors
    if (document.getElementById("tstartStop") && document.getElementById("display_timer")) {
        document.getElementById("tstartStop").addEventListener("click", tstartStop);
        
        if (document.getElementById("treset")) {
            document.getElementById("treset").addEventListener("click", treset);
        }
    }
});

// Timer function
function timer() {
    // Check if timer has reached zero
    if (tseconds === 0) {
        if (tminutes === 0) {
            if (thours === 0) {
                // Timer finished
                window.clearInterval(tinterval);
                document.getElementById("tstartStop").innerHTML = "Start";
                document.getElementById("tstartStop").className = "btn btn-outline-success btn-lg";
                tstatus = "stopped";
                
                // Alert user
                alert("Timer complete!");
                
                return;
            } else {
                thours--;
                tminutes = 59;
                tseconds = 59;
            }
        } else {
            tminutes--;
            tseconds = 59;
        }
    } else {
        tseconds--;
    }

    // Format display values
    tdisplaySeconds = tseconds < 10 ? "0" + tseconds : tseconds;
    tdisplayMinutes = tminutes < 10 ? "0" + tminutes : tminutes;
    tdisplayHours = thours < 10 ? "0" + thours : thours;

    // Display updated time values to user
    document.getElementById("display_timer").innerHTML = tdisplayHours + ":" + tdisplayMinutes + ":" + tdisplaySeconds;
}

// Function to start/stop timer
function tstartStop() {
    if (tstatus === "stopped") {
        // Get input values if they exist
        let inputSeconds = document.getElementById("tseconds");
        let inputMinutes = document.getElementById("tminutes");
        let inputHours = document.getElementById("thours");
        
        // Set initial values if inputs exist
        if (inputSeconds && inputMinutes && inputHours) {
            tseconds = parseInt(inputSeconds.value) || 0;
            tminutes = parseInt(inputMinutes.value) || 0;
            thours = parseInt(inputHours.value) || 0;
            
            // Format display values
            tdisplaySeconds = tseconds < 10 ? "0" + tseconds : tseconds;
            tdisplayMinutes = tminutes < 10 ? "0" + tminutes : tminutes;
            tdisplayHours = thours < 10 ? "0" + thours : thours;
            
            // Display initial time
            document.getElementById("display_timer").innerHTML = tdisplayHours + ":" + tdisplayMinutes + ":" + tdisplaySeconds;
        }
        
        // Check if timer has a valid value
        if (tseconds === 0 && tminutes === 0 && thours === 0) {
            alert("Please set a time before starting the timer");
            return;
        }
        
        // Start the timer
        tinterval = window.setInterval(timer, 1000);
        tstatus = "started";
        document.getElementById("tstartStop").innerHTML = "Stop";
        document.getElementById("tstartStop").className = "btn btn-outline-danger btn-lg";
    } else {
        // Stop the timer
        window.clearInterval(tinterval);
        document.getElementById("tstartStop").innerHTML = "Start";
        document.getElementById("tstartStop").className = "btn btn-outline-success btn-lg";
        tstatus = "stopped";
    }
}

// Function to reset the timer
function treset() {
    window.clearInterval(tinterval);
    
    // Reset time values
    tseconds = 0;
    tminutes = 0;
    thours = 0;
    
    // Reset display values
    document.getElementById("display_timer").innerHTML = "00:00:00";
    document.getElementById("tstartStop").innerHTML = "Start";
    document.getElementById("tstartStop").className = "btn btn-outline-success btn-lg";
    tstatus = "stopped";
    
    // Reset input fields if they exist
    let inputSeconds = document.getElementById("tseconds");
    let inputMinutes = document.getElementById("tminutes");
    let inputHours = document.getElementById("thours");
    
    if (inputSeconds && inputMinutes && inputHours) {
        inputSeconds.value = 0;
        inputMinutes.value = 0;
        inputHours.value = 0;
    }
}