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
        window.close(); // Close the popup window
        window.opener.location.reload(); // Refresh the parent window
    })
    .catch(error => {
        console.error('Error:', error);
        window.close(); // Ensure the popup closes even if there's an error
    });
}
