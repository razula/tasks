// Checks if the logged-in user is an admin and displays the delete users button accordingly.
function isAdmin(){
    axios.get("/api/session").then(response => {
        if (response.data.userSession == "admin"){
            document.getElementById("deleteUsers").style.display= "inline";
        }    
    })
}

isAdmin();

// Retrieves the list of users and creates a form for deleting users.
function deleteUsers(){
    axios.get("/api/users").then(response => {
        
        html = `<form action="/delete/users/" id="deleteUsersForm" method="GET" class="deleteUsersForm">
                    <select class=selectionDelete name="id" multiple size="4">`;

            
        response.data.allUsersDict.map(user => {
            html += `<option class="options" value="${user.id}">${user.username}</option>`;
                })
        
            html+= 
                        `</select>
                        <button onclick="deleteUsersForm.submit()">Delete</button>
                    </form>`
        
        document.getElementById("deleteDiv").innerHTML=html
    })
}

// Toggles the display of the form for adding tasks.
function addFormDiv() {
    if (document.getElementById("addFormDiv").style.display == "none") {
        document.getElementById("addFormDiv").style.display = "flex";
        document.getElementById("addFormDiv").style.flexDirection = "column";
    }
    else {document.getElementById("addFormDiv").style.display = "none";}
    
}

// Validates the fields in the add task form before submission.
function submitAddForm() {
    let valid=true;
    let html="";

    Array.from(document.getElementById("addFormDiv").getElementsByTagName("input")).map(item => {
        if (item.value == "") {
            item.style.backgroundColor = "pink";
            html = "Please fill out the red fields.";
            valid=false;
            document.getElementById("deleteDiv").innerHTML= html;
        }
        
    })
      
    Array.from(document.getElementById("addFormDiv").getElementsByTagName("select")).map(item => {
        if (item.value == "") {
            item.style.backgroundColor = "pink";
            html += "Please Select values.";
            valid=false;
            document.getElementById("deleteDiv").innerHTML= html;
        }
        
    })

    inputDate = document.getElementById("id_dueDate").value
    today = new Date()

    if (isValidDateFormat(inputDate) == false) {
        document.getElementById("id_dueDate").style.backgroundColor = "pink";
        valid=false
    }
   
    else {
        inputDate = new Date(inputDate);

        if (inputDate <= today) {
        document.getElementById("id_dueDate").style.backgroundColor = "pink";
        valid=false
        return;
    }}

    if (valid == true) {
        addForm.submit();
        addFormDiv();
        }
}

// Checks if the input date is in valid format (YYYY-MM-DD).
function isValidDateFormat(input) {

    let dateFormatRegex = /^\d{4}-\d{2}-\d{2}$/;

    return dateFormatRegex.test(input);
}

// Updates an existing task based on the provided form data.
function updateTask(taskId, dateCreated, description, dueDate, notes, status) {
        
    axios.get("/api/users").then(response => { html = 

    `<form class="updateForm" action='/update/task/' method='POST', id='updateTaskForm'>
        <div class="inUpdateForm">
        <div class="labels">
            <div>Title:</div>
            <div>Due Date:</div>
            <div>Notes:</div>
            <div>Status:</div>
        </div>
        <div class="inputs">
            <input name='taskId' value=${taskId} hidden>
            <input name='dateCreated' value=${dateCreated} hidden>
            <input name='description' value="${description}">
            <input name='dueDate' value=${dueDate}>
            <input name='notes' value="${notes}">
            <select name='status' id="selectStatusUpdate">
                <option value="${status}", selected>${status}</option>
                <option value="To do">To do</option>
                <option value="In progress">In progress</option>
                <option value="Done">Done</option>
            </select>
        </div>
        </div>
        <div class "userSelect">
        <div class="selectLabel">Press CTRL to select multiple:</div>
        <select id="selectUsersUpdate" class=selection name="users" class="options2" multiple size="4">`
            
        response.data.allUsers.map(user => {
            html += `<option class="options" value="${user}">${user}</option>`;
                
                })
        
            html+=
                    `</select>
                </div>
            </form>
            <button onclick="validateUpdateTaskForm()">Update!</button>`
        
        document.getElementById(`task${taskId}`).innerHTML= html;

        })

            
}

// Deletes a task after confirmation.
function deleteTask(taskId) {
    let confirmed = confirm("Are you sure you want to delete this task?")
    if (confirmed) {
        html = `
            <form action="/delete/task/" id=deleteForm method='GET'>
                <input name="id" value="${taskId}">
            </form>`
            
    document.getElementById("deleteDiv").innerHTML = html;
    deleteForm.submit();
    }
    else {alert("Delete Canceled");}
}


// Validates the fields in the update task form before submission.
function validateUpdateTaskForm(){
        let valid=true;
        let html="";
    
        Array.from(document.getElementById("updateTaskForm").getElementsByTagName("input")).map(item => {
            if (item.value == "") {
                item.style.backgroundColor = "pink";
                html = "Please fill out the red fields.";
                valid=false;
                document.getElementById("deleteDiv").innerHTML= html;
            }
            
        })
          
        
            if (document.getElementById("selectUsersUpdate").value == "") {
                document.getElementById("selectUsersUpdate").style.backgroundColor = "pink";
                html += "Please Select values.";
                valid=false;
                document.getElementById("deleteDiv").innerHTML= html;
            }
            
        
            if (document.getElementById("selectStatusUpdate").value == "") {
                document.getElementById("selectStatusUpdate").style.backgroundColor = "pink";
                html += "Please Select values.";
                valid=false;
                document.getElementById("deleteDiv").innerHTML = html;
            }
            

        inputDate = document.getElementById("id_dueDate").value
        today = new Date()
    
        if (isValidDateFormat(inputDate) == false) {
            document.getElementById("id_dueDate").style.backgroundColor = "pink";
            valid=false
        }
       
        else {
            inputDate = new Date(inputDate);
    
            if (inputDate <= today) {
            document.getElementById("id_dueDate").style.backgroundColor = "pink";
            valid=false
            return;
        }}
    
        if (valid == true) {
            updateTaskForm.submit();
            }
    
}
