

let button = document.getElementById("SubmitBtn");
button.onclick = function() {
let number = Math.floor(Math.random() * 10 + 1); // Generate a random number between 1 and 10
console.log(number); // Log the random number to the console for testing purposes

let randomlink = "survey_" + number + ".html"; // Create a link to the corresponding survey page
window.location.href = randomlink; // Redirect the user to the random survey page

}

//https://www.w3schools.com/jsref/jsref_random.asp
