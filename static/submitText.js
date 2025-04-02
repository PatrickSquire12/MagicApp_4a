function submitText(fileType, index, text, deckName) {
    fetch('/update_file', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ type: fileType, index: index, text: text, deckName: deckName })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        // Navigate back to the main page after submission
        window.location.href = '/';
    })
    .catch(error => {
        console.error('Error:', error);
    });
}