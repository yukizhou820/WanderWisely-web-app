function recordButton(input, select_type) {
    // Send an AJAX request to the Flask server to record the button click
    fetch('/record_button', {
        method: 'POST',
        body: JSON.stringify({ input: input, type: select_type }),
        headers: {
            'Content-Type': 'application/json'
        }
    });

}

function toggleButtonColor(button,input,type) {
    if (button.classList.contains('active')) {
        button.classList.remove('active');
    } else {
        button.classList.add('active');
    }
    recordButton(input, type);
}

function toggleButtonOne(button, input, type) {
    // Remove the "selected" class from all buttons in the group
    var buttons = document.getElementsByName(type);
    for (var i = 0; i < buttons.length; i++) {
        buttons[i].classList.remove('active');
    }
    // Add the "selected" class to the clicked button
    button.classList.add('active')

    recordButton(input, type);
}