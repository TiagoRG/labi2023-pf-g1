const dragArea = document.querySelector(".drag-area");
const dragText = document.querySelector(".header");

let button = document.querySelector(".button");
let input = document.querySelector("input");

let file;

button.onclick = () => {
	input.click();
}

// When browse button is clicked
input.addEventListener("change", function () {
	// Getting the file
	file = this.files[0];

	dragArea.classList.add("active");

	displayFile();
});

// When file is dragged over the drag area
dragArea.addEventListener("dragover", (event) => {
	event.preventDefault();
	dragText.textContent = "Release to Upload File";
	dragArea.classList.add("active");
	// console.log("File is over the drag area");
});

// When file leaves the drag area
dragArea.addEventListener("dragleave", () => {
	dragText.textContent = "Drag & Drop";
	dragArea.classList.remove("active");
	// console.log("File is outside the drag area");
});

// When file is dropped on the drag area
dragArea.addEventListener("drop", (event) => {
	event.preventDefault();

	// Getting the file
	file = event.dataTransfer.files[0];

	displayFile();
});

function displayFile() {
	let fileType = file.type;
	let validExtensions = ["image/jpeg", "image/jpg", "image/png"];

	if (validExtensions.includes(fileType)) {
		let fileReader = new FileReader();

		fileReader.onload = () => {
			let fileURL = fileReader.result;
			console.log(fileURL);
			let imgTag = `<img src="${fileURL}" alt="">`;
			console.log(imgTag);
			dragArea.innerHTML = imgTag;
		}
		fileReader.readAsDataURL(file);
	} else {
		alert("This is not an Image File!");
		dragArea.classList.remove("active");
		dragText.textContent = "Drag & Drop";
	}
}

function sendFile(file) {
	var data = new FormData();
	data.append("my_file", file);

	//Obtain nameImg and authorImg and fill the form
	var name = document.getElementById("nameImg").value;
	data.append("my_file_name", name)

	var author = document.getElementById("authorImg").value;
	data.append("my_file_author", author)

	var xhr = new XMLHttpRequest();
	xhr.open("POST", "/actions/upload_image");
	xhr.send(data);
}

function uploadImage() {
	if(file != null) {
		// Show alert to confirm the upload
		alert("Image uploaded successfully!");
		document.querySelector("#nameImg").value = "";
		document.querySelector("#authorImg").value = "";
		sendFile(file);
		//Release the resources alocated to the selected image
		window.URL.revokeObjectURL(file);
	}
	else alert("No image attached!");
}
