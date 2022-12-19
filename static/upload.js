document.getElementById("uploadfile").innerHTML = '<input type="file" id="fileInput" />';

const fileInput = document.querySelector("#fileInput");
const thumbholder = document.querySelector("#thumbholder");
const hiddenimg = document.getElementById('hiddenimages');
var imgarray = [];

const uploadFile = file => {
  console.log("Uploading file...");
  const API_ENDPOINT = "/upload";
  const request = new XMLHttpRequest();
  const formData = new FormData();
  let response = "";

  request.open("POST", API_ENDPOINT, true);
  request.onreadystatechange = () => {
    if (request.readyState === 4 && request.status === 200) {
        // This is what happens if upload worked
        console.log(request.responseText);
        response = request.responseText

        // Show thumbnail
        let thumbn = document.createElement('img');
        thumbn.src = "/thumb/" + request.responseText;
        thumbholder.appendChild(thumbn);

        // Add filename to list
        imgarray.push(request.responseText);
        hiddenimg.value = imgarray.join();
      
    }
  };
  formData.append("file", file);
  request.send(formData);
  
  


};

fileInput.addEventListener("change", event => {
  const files = event.target.files;
  uploadFile(files[0]);
});

