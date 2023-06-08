//Define variables to hold time values
let seconds = 0;
let minutes = 0;
let hours = 0;

//define vars to hold "display values"
let displaySeconds = 0;
let displayMinutes = 0;
let displayHours = 0;

//define var to hold seinterval function
let interval = null;

//define var to hold stopwatch status

let status = "stopped"

//Stopwatch function (logic to determine when to increment next value etc.)
function stopwatch() {
    seconds++

    //Logic to determine when to increment next value
    if (seconds/60 === 1) {
        seconds = 0;
        minutes++;

        if (minutes/60 === 1) {
            minutes = 0;
            hours++;
        }
    }

    //if seconds/minutes/hours is only one digit, add leading 0 to value
    if (seconds < 10) {
        displaySeconds = "0" + seconds.toString()
    }
    else {
        displaySeconds = seconds
    }
    if (minutes < 10) {
        displayMinutes = "0" + minutes.toString()
    }
    else {
        displayMinutes = minutes
    }
    if (hours < 10) {
        displayHours = "0" + hours.toString()
    }
    else {
        displayhours = hours
    }

    //Display updated time values to user
    document.getElementById("display").innerHTML = displayHours + ":" + displayMinutes + ":" + displaySeconds
}



function startStop() {
    if (status === "stopped") {
        //start the stopwatch by calling the set interval function

        interval = window.setInterval(stopwatch, 1000)
        status = "started";
        document.getElementById("startStop").innerHTML = "Stop"
        document.getElementById("startStop").className = "btn btn-outline-danger btn-lg"
    }
    else {
        window.clearInterval(interval)
        document.getElementById("startStop").innerHTML = "Start"
        document.getElementById("startStop").className = "btn btn-outline-success btn-lg"
        status = "stopped"
    }
}

//function to reset the stopwatch
function reset() {
    window.clearInterval(interval)
    seconds = 0
    minutes = 0
    hours = 0
    document.getElementById("display").innerHTML = "00:00:00"
    document.getElementById("startStop").innerHTML = "Start"
    document.getElementById("startStop").className = "btn btn-outline-success btn-lg"
}