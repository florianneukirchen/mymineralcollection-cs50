// create variables
const addInput = document.querySelector('#addInput');
const addBtn = document.querySelector('#addBtn');

function addLists() {
  if (addInput.value === '') {
    alert('Enter the list name please!!!');
  } else {
    const ul = document.getElementById('ulminerals');
    const li = document.createElement('li');
    li.innerHTML = addInput.value;
    addInput.value = '';
    ul.appendChild(li);
    createBtn(li);
  }
}

// add list when clicked on add item button
addBtn.addEventListener('click', () => {
  addLists();
});

// remove button
const listUl = document.getElementById('ulminerals');
const lis = listUl.children;

function createBtn(li) {
    // create remove button
    const remove = document.createElement('button');
    remove.className = 'btn btn-secondary';
    remove.innerHTML = 'Remove';
    li.appendChild(remove);
    return li;
}

// loop to add buttons in each li
for (var i = 0; i < lis.length; i++) {
  createBtn(lis[i]);
}

//Add button action
const divList = document.getElementById('listholder');

divList.addEventListener('click', (event) => {
  if (event.target.tagName === 'BUTTON') {
    const button = event.target;
    const li = button.parentNode;
    const ul = li.parentNode;
    if (button.className === 'btn btn-secondary') {
      ul.removeChild(li);
    } 
  }
});
