var id;

$(document).ready(
    function(){
        const params = new URLSearchParams(window.location.search);
        id = params.get("imgid");
		console.log(id);
    });

function newcomment() {
	let data = new FormData();
	data.append("imageid", id);
	let title = document.querySelector("#comment-title").value
	data.append("comment_title", title);
	let comment = document.querySelector("#comment").value
	data.append("comment", comment);
	let xhr = new XMLHttpRequest();
	xhr.open("POST", "/actions/newcomment");
	xhr.send(data);
	console.log(title);
	console.log(comment);
	console.log(xhr);
	alert("Commented!");
	document.querySelector("#comment-title").value = "";
	document.querySelector("#comment").value = "";
	window.location.reload();
}

function upvote() {
	let data = new FormData();
	data.append("imageid", id);
	let xhr = new XMLHttpRequest();
	xhr.open("POST", "/actions/upvote");
	xhr.send(data);
	alert("Upvoted!");
	window.location.reload();
}

function downvote() {
	let data = new FormData();
	data.append("imageid", id);
	let xhr = new XMLHttpRequest();
	xhr.open("POST", "/actions/downvote");
	xhr.send(data);
	alert("Upvoted!");
	window.location.reload();
}