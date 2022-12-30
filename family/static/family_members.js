//var family_members = 
//   [
//    {"username": "John", "password": "password1", "balance":7500.66, "debt":0.0},
//    {"username": "Jane", "password": "password2", "balance":3999.66, "debt":0.0},
//    {"username": "Michael", "password": "password3", "balance":333.11, "debt":50.00}, 
//    {"username": "Marie", "password": "password4", "balance":115.00, "debt":0.0},
//    {"username": "Liam", "password": "password5", "balance":99.00, "debt":75.0}, 
//   ]

function showViewAll() {
   document.getElementById('showCreateButton').style.display = "block"
   document.getElementById('family_members_table').style.display = "block"
   document.getElementById('createUpdateForm').style.display = "none"
   document.getElementById('divForTable').style.display = "block"
}

function showCreate() {
   document.getElementById('family_members_table').style.display = "none"
   document.getElementById('createUpdateForm').style.display = "block"
   document.getElementById('divForTable').style.display = "none"
   document.getElementById('createLabel').style.display = "inline"
   document.getElementById('updateLabel').style.display = "none"
   document.getElementById('showCreateButton').style.display = "none"
   document.getElementById('doCreateButton').style.display = "inline"
   document.getElementById('goBackButton').style.display = "inline"
   document.getElementById('doUpdateButton').style.display = "none"
   
}

function showUpdate(buttonElement) {
   document.getElementById('family_members_table').style.display = "none"
   document.getElementById('createUpdateForm').style.display = "block"
   document.getElementById('divForTable').style.display = "none"
   document.getElementById('createLabel').style.display = "none"
   document.getElementById('updateLabel').style.display = "inline"
   document.getElementById('showCreateButton').style.display = "none"
   document.getElementById('doCreateButton').style.display = "none"
   document.getElementById('doUpdateButton').style.display = "inline"
   document.getElementById('goBackButton').style.display = "inline"
}

function goBack() {
   window.location = '/login/login';
   return false;
}

function doCreate() {
   var form = document.getElementById('createUpdateForm')
   var new_user = {}
   family_members.username = form.querySelector('input[name="Username"]').value
   family_members.password = form.querySelector('input[name="Password"]').value
   family_members.balance = form.querySelector('select[name="Balance"]').value
   family_members.debt = form.querySelector('select[name="Debt"]').value
   createUserAjax(new_user)
}

function doUpdate() {
   var family_members = getUserFromForm();
   document.getElementById(family_members.username);
   updateUserAjax(family_members);
   clearForm();
   showViewAll();
}

function doDelete(r) {
   if (!confirm('Delete user from database?')) {
       return false;
   }
   var tableElement = document.getElementById('family_members_table');
   var rowElement = r.parentNode.parentNode;
   var index = rowElement.rowIndex;
   deleteUserAjax(rowElement.getAttribute("Username"));
   tableElement.deleteRow(index);
}

function addUserToTable(family_members) {
   var tableElement = document.getElementById('family_members_table')
   var rowElement = tableElement.insertRow(-1)
   rowElement.setAttribute('Username', family_members.username)
   var cell1 = rowElement.insertCell(0);
   cell1.innerHTML = family_members.username
   var cell2 = rowElement.insertCell(1);
   cell2.innerHTML = family_members.password
   var cell3 = rowElement.insertCell(2);
   cell3.innerHTML = family_members.balance
   var cell4 = rowElement.insertCell(3);
   cell4.innerHTML = family_members.debt
   var cell5 = rowElement.insertCell(4);
   cell5.innerHTML = '<button onclick="showUpdate(this)">Update</button>'
   var cell6 = rowElement.insertCell(5);
   cell6.innerHTML = '<button class="delete-back" onclick=doDelete(this)>Delete</button>'
}
function addSelectName(family_members) {
   var select = document.getElementById('Usernames');
   var option = document.createElement("option");
   option.text = family_members.username;
   select.add(option);
   select.options[0].selected="true";
}

host = window.location.origin
function getAllAjax() {
   $.ajax({
       "url": host+"/family_members/",
       "method": "GET",
       "data": "",
       "dataType": "JSON",
       "error": function (xhr, status, error) {
           if (xhr.status == 404) {
               alert('Page is not found');
           } else if (xhr.status == 500) {
               alert('Internal Server Error.');
           }  else if (error === 'timeout') {
               alert('Time out error');
           } else if (error === 'abort') {
               alert('Ajax request aborted');
           },
       "success": function (result) {
           //console.log(result);
           for (family_members of result) {
               addUserToTable(family_members);
           }
       }
      }
   });
}

function createUserAjax(family_members) {
   console.log(JSON.stringify(family_members));
   $.ajax({
       "url": host+"/family_members/",
       "method": "POST",
       "data": JSON.stringify(family_members),
       "dataType": "JSON",
       contentType: "application/json; charset=utf-8",
       "error": function (xhr, status, error) {
           if (xhr.status == 404) {
               alert('Page is not found');
           } else if (xhr.status == 500) {
               alert('Internal Server Error.');
           }  else if (error === 'timeout') {
               alert('Time out error');
           } else if (error === 'abort') {
               alert('Ajax request aborted');
           },
         }
       },
       "success": function (result) {
           family_members.username = result.username
           addUserToTable(family_members)
           clearForm()
           showViewAll()
      });
  }

function updateUserAjax(family_members) {
   console.log(JSON.stringify(family_members));
   $.ajax({
       "url": host+"/family_members/"+encodeURI(family_members.username),
       "method": "PUT",
       "data": JSON.stringify(family_members),
       "dataType": "JSON",
       contentType: "application/json; charset=utf-8",
       "error": function (xhr, status, error) {
         if (xhr.status == 404) {
            alert('Page is not found');
        } else if (xhr.status == 500) {
            alert('Internal Server Error.');
        }  else if (error === 'timeout') {
            alert('Time out error');
        } else if (error === 'abort') {
            alert('Ajax request aborted');
        },
      }
    },
    "success": function (result) {
           console.log("AJAX UPDATE: " + JSON.stringify(family_members));
   });
}

function deleteUserAjax(username) {
   $.ajax({
       "url": host+"/family_members/"+encodeURI(username),
       "method": "DELETE",
       "data": "",
       "dataType": "JSON",
       contentType: "application/json; charset=utf-8",
       "error": function (xhr, status, error) {
         if (xhr.status == 404) {
            alert('Page is not found');
        } else if (xhr.status == 500) {
            alert('Internal Server Error.');
        }  else if (error === 'timeout') {
            alert('Time out error');
        } else if (error === 'abort') {
            alert('Ajax request aborted');
        },
      }
    },
       "success": function (result) {
   });
}

getAllAjax();