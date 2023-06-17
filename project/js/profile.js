
let container = document.getElementById("container");
let nav = document.getElementById("navbar");

function showNav() {
    if (container.scrollTop > 280) {
        nav.style.zIndex = "1";
    } else {
        nav.style.zIndex = "-1";
    }
}

function scrollUP() {
    container.scrollTop = 0;
}

var currentDiv = null;

function toggleDiv(divId) {
  var div = document.getElementById(divId);

  if (currentDiv !== null) {
    currentDiv.style.display = 'none';
  }

  div.style.display = 'flex';
  currentDiv = div;
}

toggleDiv('posts');