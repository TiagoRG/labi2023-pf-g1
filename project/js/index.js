var loginId = document.getElementById("login");
var registerId = document.getElementById("register");
var btnId = document.getElementById("btn");

function register(){
    loginId.style.left = "-120%";
    registerId.style.left = "8%";
    btnId.style.left = "50%";
}
function login(){
    loginId.style.left = "8%";
    registerId.style.left = "120%";
    btnId.style.left = "0%";
}

function showPopup() {
    document.getElementById("popup1").style.animation = "fadeIn 0.5s";
    document.getElementById("popup1").style.opacity = "1";
    document.getElementById("popup1").style.display = "block";
}

function hidePopup() {
    document.getElementById("popup1").style.animation = "fadeOut 0.5s";
    document.getElementById("popup1").style.opacity = "0";
    setTimeout(() => {document.getElementById("popup1").style.display = "none"}, 500) // wait for 500ms


}

function done() { function done() {
    document.getElementById("popup").style.display = "none";
    var password = document.getElementById("pass").value;

    //DO STUFF WITH PASSWORD HERE
}
}