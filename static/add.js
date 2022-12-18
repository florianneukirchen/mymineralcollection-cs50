// Magic search
let input = document.getElementById('mininput');
input.addEventListener('input', async function() {
    let response = await fetch('/mineralsearch?q=' + input.value);
    let searchresult = await response.json();
    let html = '';
    for (let id in searchresult) {
        let title = searchresult[id].name;
        html += '<button type=\"button\" onclick=\"addtolist(id)\" class=\"addBtn list-group-item list-group-item-action\" id=\"' + title + '\">' + title + '</button>';
    }
    
    console.log(html);
    document.getElementById("present").innerHTML = html;
});

// Add to list

var addBtns = document.querySelectorAll('.addBtn');

// function triggered by click event

function addtolist(value) {
  const ul = document.getElementById('ulminerals');
  const li = document.createElement('li');
  li.innerHTML = value;
  addInput.value = '';
  ul.appendChild(li);
  // Create delete button
  createBtn(li);
  
}




 
