$(document).ready(function(){
    $(".page-title-section").height($(window).height());
    $(".page-title-spacer").height(($(window).height()-$(".page-title").height())/2);
});

let footer_content = document.getElementById("footer");
let container = document.getElementById("container");

container.onscroll = (() => {
    if (container.scrollTop >= 1 || container.scrollTop >= 1) {
        footer_content.style.backgroundColor = "rgba(17, 16, 29, 0.75)";
        footer_content.style.color = "white";
        changeFooterLinkColor(1)
    }
    else {
        footer_content.style.backgroundColor = "rgba(255, 255, 255, 0)";
        footer_content.style.color = "black";
        changeFooterLinkColor(0)
    }
});

function changeFooterLinkColor(color) {
    let footer_links = document.querySelectorAll(".footer-link");
    for (let i = 0; i < footer_links.length; i++) {
        if (color === 1)
            footer_links[i].style.color = "#96b9d9";
        else
            footer_links[i].style.color = "#5f5b91";
    }
}

function goToSection(id) {
    $('.about-container').animate({
        scrollTop: $(id).offset().top - 25
    }, 500);
}

let popupActive = false;
let lastPopup = null;

$(document).keydown(function (key) {
    if (popupActive) {
        if (key.keyCode === 27) {
            closePopup();
        }
        else if (key.keyCode === 37 || key.keyCode === 39 || key.keyCode === 65 || key.keyCode === 68) {
            switchPopup();
        }
    }
});

function openPopup(id, fade = 250) {
    $('#popups').fadeIn(fade);
    lastPopup = id;
    $(id).fadeIn(fade);
    popupActive = true;
}

function closePopup(fade = 250) {
    $('#popups').fadeOut(fade);
    $(lastPopup).fadeOut(fade);
    popupActive = false;
}

function switchPopup() {
    closePopup(0);
    openPopup(lastPopup === "#project-description" ? "#project-roadmap" : "#project-description", 0);
}