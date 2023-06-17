

var currentDiv = null;

function toggleDiv(divId) {
  var div = document.getElementById(divId);

  if (currentDiv !== null) {
    currentDiv.style.display = 'none';
  }

  div.style.display = 'flex';
  currentDiv = div;
}

// Initially show the first div
toggleDiv('posts');


