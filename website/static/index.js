// Handler for deleting posts.
function deletePost(id){
    fetch('/deletePost', {method: 'POST', body: JSON.stringify({postId: id})}).then((_res) => {
        window.location.href = '/';
    });
}

// Handler for deleting posts.
function deleteUser(id){
    fetch('/deleteUser', {method: 'POST', body: JSON.stringify({userId: id})}).then((_res) => {
        window.location.href = '/admin';
    });
}

// Handler for deleting posts.
function editPost(id){
    fetch('/editPost', {method: 'POST', body: JSON.stringify({postId: id})}).then((_res) => {
        window.location.href = '/editPost';
    })
}

// Handler for editing text.
function editText(id){
    // Creating a textarea, replace the current <p> with it and fill it with the existing text.
    let item = document.getElementById(id).getElementsByTagName('p')[0]
    let currentText = item.innerText;
    let input = document.createElement('textarea');
    input.innerText = currentText;
    item.appendChild(input);
    item.hidden = true;
    item.parentNode.insertBefore(input, item); 
    input.classList += "form-control";
    input.style = "resize: auto;"
    input.value = currentText;
    let saveButton = document.createElement("button");
    saveButton.classList += "btn";
    saveButton.classList += "btn-primary";
    saveButton.innerText = "Save";
    // Add event handler for when save button is clicked, to send data to save post.
    saveButton.addEventListener('click', function(){
        fetch('/updatePost', {method: 'POST', body: JSON.stringify({postId: id, newbody: input.value})}).then((_res) => {
            window.location.href = '/';
        });
    })
    insertAfter(saveButton, input)
}

// Custom function to insert element after another one.
function insertAfter(newNode, referenceNode) {
    referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
}