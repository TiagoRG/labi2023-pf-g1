$('.nav ul li').click(function(){

    $(this).addClass("active").siblings().removeClass('active');
})

const tabBtn = document.querySelectorAll('.nav ul li');
const tab = document.querySelectorAll('.tab');

function tabs(panelIndex){
    tab.forEach(function(node){
        node.style.display = 'none';

    });
    tab[panelIndex].style.display = 'block';
}
tabs(0);
function showPopup() {
     document.getElementById("popup").style.display = "block";
}

function done() { function done() {
    document.getElementById("popup").style.display = "none";
    var password = document.getElementById("pass").value;

    //DO STUFF WITH PASSWORD HERE
}
}

