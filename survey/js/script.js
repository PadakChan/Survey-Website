

let button = document.getElementById("SubmitBtn");
button.onclick = function () {
    let number = Math.floor(Math.random() * 10 + 1); // Generate a random number between 1 and 10
    console.log(number); // Log the random number to the console for testing purposes

    let randomlink = "survey_" + number + ".html"; // Create a link to the corresponding survey page
    window.location.href = randomlink; // Redirect the user to the random survey page

}
//use list to randomnize the site instead of using number to link the page. 
let survey = [
    "survey_1.html",
    "survey_2.html",
    "survey_3.html",
    "survey_4.html",
    "survey_5.html",
    "survey_6.html",
    "survey_7.html",
    "survey_8.html",
    "survey_9.html",
    "survey_10.html"
]

console.log(survey.length);
console.log(survey[0]);

for (let i = 0; i < survey.length; i++) {
    let j = Math.floor(Math.random() * survey.length);
    let temp = survey[i];
    survey[i] = survey[j];
    survey[j] = temp;
    console.log(survey[j]);
}

function shuffle(array) {

    for (let i = array.lenth - 1; i > 0; i--) {
        let j = Math.floor(Math.random() * (i + 1));
        let temp = array[i];
        array[i] = array[j];
        array[j] = temp;
    }
}

let currentSurvey = 0;

button.onclick = function () {

    let nextSurvey = surveys[currentIndex];
    currentIndex++;
    window.location.href = nextSurvey;

};
//https://www.w3schools.com/jsref/jsref_random.asp
