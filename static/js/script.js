// NAVIGATION (HOME PAGE) 

// go to survey start (Flask handles random)
let Surveybutton = document.getElementById("SurveyBtn");
if (Surveybutton) {
    Surveybutton.onclick = function () {
        // window.location.href = "survey/intro.html"; 
        window.location.href = "/start";
    };
}

// go to about page
let AboutButton = document.getElementById("AboutBtn");
if (AboutButton) {
    AboutButton.onclick = function () {
        window.location.href = "/about";
    };
}

// LIGHT SWITCH (Home Page DO NOT TOUCH - I just got this from YouTube)
let btn = document.querySelector(".btn");
let body = document.body;

if (btn) {
    btn.addEventListener("click", () => {
        body.classList.toggle("on"); // turn light on/off
    });
}

// DRAG EMOTION MAP
//inspired from Application Dev class for Heart Moving Map, but I made it more complex by adding the percentage calculation and live update.
// I also added a fading effect when the submit button is clicked to make it more visually appealing.
// get dot and map
let dot = document.getElementById("dot");
let map = document.getElementById("emotionMap");
// store dragging state
let isDragging = false;

// start dragging
if (dot && map) {
    // when the mouse button is pressed down on the dot, set isDragging to true
    dot.addEventListener("mousedown", function () {
        isDragging = true;
    });

    // stop dragging
    document.addEventListener("mouseup", function () {
        isDragging = false;
    });

    // move dot
    document.addEventListener("mousemove", function (event) {
        if (!isDragging) return;
        // find the emotion box and calculate the mouse position relative to the emotion box
        let rect = map.getBoundingClientRect(); //getBoundingClientRect() is a method that returns the size of an element and its position relative to the viewport. It returns an object with properties like left, top, right, bottom, width, and height.
        //https://www.w3schools.com/jsref/met_element_getboundingclientrect.asp
        let x = event.clientX - rect.left;
        let y = event.clientY - rect.top;

        // keep inside box
        x = Math.max(0, Math.min(x, rect.width));
        y = Math.max(0, Math.min(y, rect.height));

        dot.style.left = x + "px"; //Move the dot to the new position by setting its left and top style properties to the calculated x and y values in pixels.
        dot.style.top = y + "px";

        // update live percentage
        updateEmotionPercent();
    });
}


// SEND DATA TO FLASK 

function sendData() {

    let textInput = document.getElementById("emotionText");

    // if not survey page, stop
    if (!textInput || !dot || !map) return;

    let text = textInput.value;

    let rect = map.getBoundingClientRect();

    let x = dot.offsetLeft;
    let y = dot.offsetTop;

    // calculate %
    //tofixed is used to round the number to 1 decimal place for better readability
    let happy = ((1 - (y / rect.height)) * 100).toFixed(1);
    let sad = ((y / rect.height) * 100).toFixed(1);
    let fear = ((1 - (x / rect.width)) * 100).toFixed(1);
    let anger = ((x / rect.width) * 100).toFixed(1);

    // send to Flask
    return fetch("/submit", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ //stringify is used to convert the JavaScript object into a JSON string that can be sent to the server. 
            text: text,
            happy: happy + "%",
            sad: sad + "%",
            fear: fear + "%",
            anger: anger + "%"
        })
    });
}


//  SUBMIT BUTTON (INTRO + SURVEY)

let button = document.getElementById("SubmitBtn");
let fadeScreen = document.getElementById("fadeScreen");

if (button) {
    button.onclick = async function () { //async is used to make the function asynchronous
//https://www.geeksforgeeks.org/javascript/asynchronous-javascript/
        if (document.getElementById("emotionText") && dot && map) {
            await sendData(); //await is used to wait for the sendData() function
        }

        if (fadeScreen) {
            fadeScreen.style.opacity = "1";
        }

        setTimeout(() => {
            window.location.href = "/next";
        }, 5000); //5seconds to read the message and see the fading effect before moving to the next page
    };
}

//  HOME BUTTON (SURVEY + THANK YOU)
let homeBtn = document.getElementById("homeBtn");

homeBtn.onclick = function () {
    window.location.href = "/";
};



// let Surveybutton = document.getElementById("SurveyBtn");
// Surveybutton.onclick = function () {
//     window.location.href = "survey/intro.html"; // Redirect the user to the random survey page

// }

// let AboutButton = document.getElementById("AboutBtn");
// AboutButton.onclick = function () {
//     window.location.href = "about.html"; // Redirect the user to the about page
// }

// let btn = document.querySelector(".btn");
// let body = document.body;

// btn.addEventListener("click", () => {
//     body.classList.toggle("on");
// });

// //list 


// // let button = document.getElementById("SubmitBtn");
// // button.onclick = function () {
// //     let number = Math.floor(Math.random() * 10 + 1); // Generate a random number between 1 and 10
// //     console.log(number); // Log the random number to the console for testing purposes

// //     let randomlink = "survey_" + number + ".html"; // Create a link to the corresponding survey page
// //     window.location.href = randomlink; // Redirect the user to the random survey page

// // } //This is dumb idea... Nedd to figure different way to randomize the survey page.


// // //use list to randomnize the site instead of using number to link the page. 
// // let survey = [
// //     "survey_1.html",
// //     "survey_2.html",
// //     "survey_3.html",
// //     "survey_4.html",
// //     "survey_5.html",
// //     "survey_6.html",
// //     "survey_7.html",
// //     "survey_8.html",
// //     "survey_9.html",
// //     "survey_10.html"
// // ]

// // console.log(survey.length);
// // console.log(survey[0]);

// // for (let i = 0; i < survey.length; i++) {
// //     let j = Math.floor(Math.random() * survey.length);
// //     let temp = survey[i];
// //     survey[i] = survey[j];
// //     survey[j] = temp;
// //     console.log(survey[j]);
// // }

// // function shuffle(array) {

// //     for (let i = array.lenth - 1; i > 0; i--) {
// //         let j = Math.floor(Math.random() * (i + 1));
// //         let temp = array[i];
// //         array[i] = array[j];
// //         array[j] = temp;
// //     }
// // }

// // let currentSurvey = 0;

// // button.onclick = function () {

// //     let nextSurvey = surveys[currentIndex];
// //     currentIndex++;
// //     window.location.href = nextSurvey;

// // };

// let surveys = JSON.parse(localStorage.getItem("surveys")); // Retrieve the surveys array from localStorage and parse it back into a JavaScript array

// let defaultSurveys = [ // Define the default list of survey pages
//     "survey_1.html",
//     "survey_2.html",
//     "survey_3.html",
//     "survey_4.html",
//     "survey_5.html"
// ];

// if (!surveys || surveys.some(item => !defaultSurveys.includes(item))) { // Check if surveys is null or if it contains any items that are not in the defaultSurveys array
//     surveys = defaultSurveys;
//     localStorage.setItem("surveys", JSON.stringify(surveys)); // If surveys is null or contains invalid items, reset it to the defaultSurveys array and store it in localStorage
// }

// let button = document.getElementById("SubmitBtn"); // Get the button element with the ID "SubmitBtn" and store it in the variable "button"
// let fadeScreen = document.getElementById("fadeScreen"); // Get the element with the ID "fadeScreen" and store it in the variable "fadeScreen" for later use in fading effect

// button.onclick = function () {
//     console.log("Working"); // Log a message to the console for testing purposes    
//     fadeScreen.style.opacity = "1"; // Set the opacity of the fadeScreen element to 1 to create a fading effect
//     setTimeout(() => { // After a delay of 5 seconds, execute the following code

//         if (surveys.length === 0) { // Check if the surveys array is empty, which means all surveys have been completed
//             localStorage.removeItem("surveys"); // Remove the surveys item from localStorage to reset the survey list for future users
//             // alert("Thank you for completing all the surveys!");
//             window.location.href = "thankyou.html"; // Redirect the user to a thank you page after completing all surveys
//             return;
//         }

//         let randomIndex = Math.floor(Math.random() * surveys.length); // Generate a random index to select a survey from the surveys array

//         let chosenSurvey = surveys[randomIndex]; // Get the survey at the random index from the surveys array and store it in the variable "chosenSurvey"

//         surveys.splice(randomIndex, 1); // Remove the chosen survey from the surveys array

//         localStorage.setItem("surveys", JSON.stringify(surveys)); // Store the updated surveys array in localStorage

//         window.location.href = chosenSurvey; // Redirect the user to the chosen survey
//     }, 5000);
// };
//  //emotion map insipired by Applicatio Dev class for Heart Moving Map
// let dot = document.getElementById("dot");
// let map = document.getElementById("emotionMap");
// // find the dot and emotion box

// let isDragging = false;
// //Store the state of dragging

// dot.addEventListener("mousedown", function () {
//     isDragging = true;
// });
// //When the mouse button is pressed down on the dot, set isDragging to true

// document.addEventListener("mouseup", function () {
//     isDragging = false;
// })
// //draging stopes

// document.addEventListener("mousemove", function (event) {
//     if (!isDragging) return; //if not dragging, do nothing

//     let rect = map.getBoundingClientRect();//find the emotion box
//     let x = event.clientX - rect.left; //Calculate the x position of the mouse relative to the emotion box
//     let y = event.clientY - rect.top; //Calculate the y position of the mouse relative to the emotion box

//     x = Math.max(0, Math.min(x, rect.width)); //Constrain x to be within the emotion box
//     y = Math.max(0, Math.min(y, rect.height)); //Constrain y to be within the emotion box

//     dot.style.left = x + "px";
//     dot.style.top = y + "px";
//     //Move the dot to the new position
// });


// //https://www.w3schools.com/jsref/jsref_random.asp


