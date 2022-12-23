function checkAll(){
  let cbs = document.querySelectorAll('.mycheckboxes');
  for (const cb of cbs){
      cb.checked = true;
  }
}

function uncheckAll(){
  let cbs = document.querySelectorAll('.mycheckboxes');
  for (const cb of cbs){
      cb.checked = false;
  }
}

function deleteselected(){
  $('#exampleModal').modal('hide');
  let cbs = document.querySelectorAll('.mycheckboxes');
  const API_ENDPOINT = "/delete";
  let ids = [];
  for (const cb of cbs){
      if (cb.checked) {
        ids.push(cb.value);
      }
    }
    
  const request = new XMLHttpRequest();
  const formData = new FormData();
  formData.append("ids", ids);

  request.open("POST", API_ENDPOINT, true);
  request.onreadystatechange = () => {
  if (request.readyState === 4 && request.status === 200) {
    console.log(request.responseText);
    for (const id of ids){
      const tablerow = document.getElementById('tr' + id);
      const parent = tablerow.parentNode;
      parent.removeChild(tablerow);
    } 
    
    }
  }
request.send(formData);

uncheckAll();
}





function deleteimage(img) {
  const API_ENDPOINT = "/deleteimg";
  const request = new XMLHttpRequest();
  const formData = new FormData();
  formData.append("img", img);
  formData.append("specimen_id", specimen_id);

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

function sortTable(n) {
    var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
    table = document.getElementById("mytable");
    switching = true;
    // Set the sorting direction to ascending:
    dir = "asc";
    /* Make a loop that will continue until
    no switching has been done: */
    while (switching) {
      // Start by saying: no switching is done:
      switching = false;
      rows = table.rows;
      // check if column is ID
      const columnid = rows[0].getElementsByTagName("TH")[n].id;
      /* Loop through all table rows (except the
      first, which contains table headers): */
      for (i = 1; i < (rows.length - 1); i++) {
        // Start by saying there should be no switching:
        shouldSwitch = false;
        /* Get the two elements you want to compare,
        one from current row and one from the next: */
        x = rows[i].getElementsByTagName("TD")[n];
        y = rows[i + 1].getElementsByTagName("TD")[n];
        /* Check if the two rows should switch place,
        based on the direction, asc or desc: */
        if (dir == "asc" && columnid != "IDColumn") {
          if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
            // If so, mark as a switch and break the loop:
            shouldSwitch = true;
            break;
          }
        } else if (dir == "desc" && columnid != "IDColumn") {
          if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
            // If so, mark as a switch and break the loop:
            shouldSwitch = true;
            break;
          }
        } else if (dir == "asc" && columnid == "IDColumn") {
          if (parseInt(x.innerHTML) > parseInt(y.innerHTML)) {
            // If so, mark as a switch and break the loop:
            shouldSwitch = true;
            break;
          }
        } else if (dir == "desc" && columnid == "IDColumn") {
          if (parseInt(x.innerHTML) < parseInt(y.innerHTML)) {
            // If so, mark as a switch and break the loop:
            shouldSwitch = true;
            break;
          }
        }
      }
      if (shouldSwitch) {
        /* If a switch has been marked, make the switch
        and mark that a switch has been done: */
        rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
        switching = true;
        // Each time a switch is done, increase this count by 1:
        switchcount ++;
      } else {
        /* If no switching has been done AND the direction is "asc",
        set the direction to "desc" and run the while loop again. */
        if (switchcount == 0 && dir == "asc") {
          dir = "desc";
          switching = true;
        }
      }
    }
  }