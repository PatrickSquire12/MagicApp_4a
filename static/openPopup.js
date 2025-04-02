function openPopup(fileType, index) {
    if (fileType === 'Deck') {
        window.location.href = `deck.html?index=${index}`;
    } else if (fileType === 'Collection') {
        window.location.href = 'collection.html';
    }
}