console.log(document);
//document = the whole HTML page

document.getElementById("")
//“Go find the HTML element with this specific ID.”

let Emotion = getElementById("") 
// using varibable to store the element for later use

document.getElementsByClassName("")
//“Go find all the HTML elements with this specific class name.”

document.getElementsByTagName("")
//“Go find all the HTML elements with this specific tag name.”

document.querySelector("")
//“Go find the first HTML element that matches this CSS selector.”

document.querySelectorAll("")
//“Go find all the HTML elements that match this CSS selector.”

onclick = function() {
    // code to execute when the element is clicked
}

onmouseover = function() {
    // code to execute when the mouse hovers over the element
}

onmouseout = function() {
    // code to execute when the mouse leaves the element
}

onkeydown = function() {
    // code to execute when a key is pressed down
}

onkeyup = function() {
    // code to execute when a key is released
}

onchange = function() {
    // code to execute when the value of an input element changes
}

onsubmit = function() {
    // code to execute when a form is submitted
}

function myFunction() {
    // code to execute when the function is called
}

let input = document.getElementById("emotionInput");

let emotion = input.value;// Get the value entered in the input field

addEventListener //Hover, click, keydown, keyup, change, submit