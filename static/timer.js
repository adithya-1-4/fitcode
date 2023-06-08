//Define variables to hold time values
let tseconds = document.querySelector("#tseconds").value;
let tminutes = document.querySelector("#tminutes").value;
let thours = document.querySelector("#thours").value;

//define vars to hold "display values"
let tdisplaySeconds = document.querySelector("#tseconds").value;;
let tdisplayMinutes = document.querySelector("#tminutes").value;;
let tdisplayHours = document.querySelector("#thours").value;;

//define var to hold seinterval function
let tinterval = null;

//define var to hold stopwatch status

let tstatus = "stopped"

//Stopwatch function (logic to determine when to increment next value etc.)
function timer() {
    if (tseconds === 0) {
        if (tminutes === 0) {
            if (thours > 0) {
                thours = thours - 1
                tminutes = 59
                tseconds = 59
            }
            else {
                STOP
            }
        }
        else {
            tminutes = tminutes - 1
            tseconds = 59
        }

    }
    else {
        tseconds = tseconds - 1
    }

    tseconds--
    //if seconds/minutes/hours is only one digit, add leading 0 to value
    if (tseconds < 10) {
        tdisplaySeconds = "0" + tseconds.toString()
    }
    else {
        tdisplaySeconds = tseconds
    }
    if (tminutes < 10) {
        tdisplayMinutes = "0" + tminutes.toString()
    }
    else {
        tdisplayMinutes = tminutes
    }
    if (thours < 10) {
        tdisplayHours = "0" + thours.toString()
    }
    else {
        tdisplayHours = thours
    }

    //Display updated time values to user
    document.getElementById("display_timer").innerHTML = tdisplayHours + ":" + tdisplayMinutes + ":" + tdisplaySeconds
}



function tstartStop() {
    if (tstatus === "stopped") {
        //start the stopwatch by calling the set interval function

        tinterval = window.setInterval(timer, 1000)
        tstatus = "started";
        document.getElementById("tstartStop").innerHTML = "Stop"
        document.getElementById("tstartStop").className = "btn btn-outline-danger btn-lg"
    }
    else {
        window.clearInterval(tinterval)
        document.getElementById("tstartStop").innerHTML = "Start"
        document.getElementById("tstartStop").className = "btn btn-outline-success btn-lg"
        tstatus = "stopped"
    }
}

//function to reset the stopwatch
function treset() {
    window.clearInterval(tinterval)
    document.getElementById("display_timer").innerHTML = "00:00:00"
    document.getElementById("tstartStop").innerHTML = "Start"
    document.getElementById("tstartStop").className = "btn btn-outline-success btn-lg"
}