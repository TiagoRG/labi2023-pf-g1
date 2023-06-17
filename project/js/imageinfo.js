var id;

$(document).ready(
    function(){
        const params = new URLSearchParams(window.location.search);
        id = params.get("id");
        imagecomments ();
    });

function imagecomments() {
	$.get("/comments",
		{ idimg : id },
		function(response){
			showimageandinfo(response);
		});
}

function showimageandinfo(response) {
	// response.image is the image information
	// response.comments is the image list comments
	// response.votes is the image votes
	document.getElementById("title").innerHTML = response.image.title + " by " + response.image.username + " on " + response.image.date;
	document.getElementById("image").src = response.image.path;
	for (var i = 0; i < response.comments.length; i++) {
		var tag = document.createElement("p");
		var text = document.createTextNode(response.comments[i].username + ": " + response.comments[i].comment + " on " + response.comments[i].date);
		tag.appendChild(text);

		var element = document.getElementById("comments");
		element.appendChild(tag);
	}
	document.getElementById("upvotes").innerHTML = "Votes: " + response.votes.ups;
	document.getElementById("downvotes").innerHTML = "Votes: " + response.votes.downs;
}

function newcomment() {
	// obtain the user and comment from image page
	var user = $.get("/get_logged_user");
	var comment = document.getElementById("comment");
    $.post("/newcomment",
        { idimag: id, username: user, newcomment: comment },

        function() { imagecomments(); }
	);
}

var upvoted = localStorage.getItem("upvote");
var downvoted = localStorage.getItem("downvote");

function upvote() {
	$.post("/upvote",
		{ idimag: id },
		function(response){
			upvoted = !this.upvoted;
			downvoted = false;
		});
}

function downvote() {
	$.post("/downvote",
		{ idimag: id },
		function(response)
		{
			downvoted = !this.downvoted;
			upvoted = false;
		});
}