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
}

function closeNav() {
    document.getElementById("mySidebar").style.width = "0";
    document.getElementById("main").style.marginLeft= "0";
}
