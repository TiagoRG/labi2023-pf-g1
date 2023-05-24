var x = document.getElementById("login");
var y = document.getElementById("register");
var z = document.getElementById("btn");

function register(){
    x.style.left = "-120%";
    y.style.left = "8%";
    z.style.left = "50%";
    y.style.up = "50%";
}
function login(){
    x.style.left = "8%";
    y.style.left = "120%";
    z.style.left = "0%";
}
function showPopup() {
     document.getElementById("popup").style.display = "block";
}
function done() { function done() {
    document.getElementById("popup").style.display = "none";
    var password = document.getElementById("pass").value;

    //DO STUFF WITH PASSWORD HERE
}
}