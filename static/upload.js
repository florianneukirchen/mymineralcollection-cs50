document.getElementById("uploadfile").innerHTML = '<input type="file" id="fileInput" />';

const fileInput = document.querySelector("#fileInput");
const thumbholder = document.querySelector("#thumbholder");
const hiddenimg = document.getElementById('hiddenimages');
const togglevis = document.getElementById("togglevis");
const specimen_id = document.getElementById("specimen_id").value; 

var imgarray = [];

// Edit: show existing images
if (hiddenimg.value) {
    imgarray = hiddenimg.value.slice(0,-1).split(','); // slice: remove , from end
    for (let img of imgarray){
        let thumbn = document.createElement('img');
        thumbn.src = "/thumb/" + img;
        thumbn.className = "m-1";
        thumbn.id = img;
        thumbn.addEventListener('click', function(){ deleteimage(img) }); 
        thumbholder.appendChild(thumbn);
        togglevis.style.visibility = 'visible';
    }

}

// Upload

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
        response = request.responseText;

        // Show thumbnail
        let thumbn = document.createElement('img');
        thumbn.src = "/thumb/" + request.responseText;
        thumbn.className = "m-1";
        thumbn.id = request.responseText;
        thumbn.addEventListener('click', function(){ deleteimage(request.responseText) }); 
        thumbholder.appendChild(thumbn);
        togglevis.style.visibility = 'visible';

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

// Delete image

function deleteimage(img) {
  const API_ENDPOINT = "/deleteimg";
  const request = new XMLHttpRequest();
  const formData = new FormData();
  formData.append("img", img);
  formData.append("specimen_id", specimen_id);
  let response = "";

  request.open("POST", API_ENDPOINT, true);
  request.onreadystatechange = () => {
    if (request.readyState === 4 && request.status === 200) {
      console.log(request.responseText);
      thumbn = document.getElementById(img);
      thumbholder.removeChild(thumbn);
      imgarray.filter(e => e != img);
      hiddenimg.value = imgarray.join();
    }
  }
  request.send(formData);
}

