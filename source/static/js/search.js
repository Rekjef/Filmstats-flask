function buttonClick(){
    var url = document.getElementById("inputURL").value;
    window.location = "/search/" + url;
}

//creates a listener for when you press a key
window.onkeyup = keyup;

//creates a global Javascript variable
var inputTextValue;

function keyup(e) {
    inputTextValue = e.target.value;
    console.log(inputTextValue);
    if (e.keyCode == 13) {
        window.location = "http://www.myurl.com/search/" + inputTextValue;
    }
}