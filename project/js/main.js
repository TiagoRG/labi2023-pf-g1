let menuOpen = false; // variável para rastrear o estado do menu

function toggleNav() {
    if (!menuOpen) {
        openNav();
    } else {
        closeNav();
    }
    menuOpen = !menuOpen; // inverta o estado do menu
}

function openNav() {
    document.getElementById("mySidebar").style.width = "250px";
    document.getElementById("main").style.marginLeft = "250px";
    document.getElementById("mainFooter").style.marginLeft = "250px";
}

function closeNav() {
    document.getElementById("mySidebar").style.width = "0";
    document.getElementById("main").style.marginLeft= "0";
    document.getElementById("mainFooter").style.marginLeft= "0";
}

window.addEventListener('click', function(e) {
    if (!document.getElementById('mySidebar').contains(e.target) &&
        !document.querySelector('.openbtn').contains(e.target) &&
        menuOpen) {
        closeNav();
        menuOpen = false;
    }
});

window.addEventListener('scroll', function() {
    if (menuOpen) {
        closeNav();
        menuOpen = false;
    }
});
