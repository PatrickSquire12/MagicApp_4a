function openPopup(fileType, index) {
    let message = fileType === 'Collection' ? `Paste your text for ${fileType} here:` : `Paste your text for ${fileType} ${index} here:`;
    const popup = window.open("", "Popup", "width=600,height=400");

    popup.onload = function() {
        setTimeout(() => {
            if (fileType === 'Deck') {
                fetch(`/get_deck_data?index=${index}`)
                    .then(response => response.json())
                    .then(data => {
                        const deckName = data.deckName || '';
                        const deckContent = data.deckContent || '';
                        popup.document.write(`
                            <html>
                                <head>
                                    <title>Paste Text</title>
                                    <style>
                                        body {
                                            font-family: 'Roboto Condensed', sans-serif;
                                            background-color: rgb(145, 139, 238); /* Same shade of purple */
                                            padding: 20px;
                                        }
                                        h3 {
                                            color: #333;
                                        }
                                        textarea {
                                            width: 100%;
                                            padding: 10px;
                                            margin-bottom: 10px;
                                            border: 1px solid #ccc;
                                            border-radius: 5px;
                                            box-sizing: border-box;
                                            rows: 10; /* Adjust the number of rows to make it shorter */
                                        }
                                        input {
                                            width: 100%;
                                            padding: 10px;
                                            margin-bottom: 10px;
                                            border: 1px solid #ccc;
                                            border-radius: 5px;
                                            box-sizing: border-box;
                                        }
                                        button {
                                            background-color: white; /* Set background to white */
                                            color: rgb(255, 87, 87); /* Set text color to orange */
                                            border: 2px solid rgb(255, 87, 87); /* Add a border with the same orange color */
                                            border-radius: 5px; /* Add border radius for rounded corners */
                                            padding: 10px 20px;
                                            cursor: pointer;
                                        }
                                        button:hover {
                                            background-color: rgb(255, 87, 87); /* Change background color on hover */
                                            color: white; /* Change text color to white on hover */
                                        }
                                    </style>
                                </head>
                                <body>
                                    <h3>${message}</h3>
                                    <input type="text" id="deckName" placeholder="Enter Deck Name" value="${deckName}"><br>
                                    <textarea id="textContent" rows="10" cols="60">${deckContent}</textarea><br>
                                    <button onclick="submitAndClose('${fileType}', ${index}, document.getElementById('textContent').value, document.getElementById('deckName').value);">Submit</button>
                                </body>
                            </html>
                        `);
                    });
            } else if (fileType === 'Collection') {
                fetch(`/get_collection_data`)
                    .then(response => response.json())
                    .then(data => {
                        const collectionContent = data.collectionContent || '';
                        popup.document.write(`
                            <html>
                                <head>
                                    <title>Paste Text</title>
                                    <style>
                                        body {
                                            font-family: 'Roboto Condensed', sans-serif;
                                            background-color: rgb(145, 139, 238); /* Same shade of purple */
                                            padding: 20px;
                                        }
                                        h3 {
                                            color: #333;
                                        }
                                        textarea {
                                            width: 100%;
                                            padding: 10px;
                                            margin-bottom: 10px;
                                            border: 1px solid #ccc;
                                            border-radius: 5px;
                                            box-sizing: border-box;
                                            rows: 10; /* Adjust the number of rows to make it shorter */
                                        }
                                        button {
                                            background-color: white; /* Set background to white */
                                            color: rgb(255, 87, 87); /* Set text color to orange */
                                            border: 2px solid rgb(255, 87, 87); /* Add a border with the same orange color */
                                            border-radius: 5px; /* Add border radius for rounded corners */
                                            padding: 10px 20px;
                                            cursor: pointer;
                                        }
                                        button:hover {
                                            background-color: rgb(255, 87, 87); /* Change background color on hover */
                                            color: white; /* Change text color to white on hover */
                                        }
                                    </style>
                                </head>
                                <body>
                                    <h3>${message}</h3>
                                    <textarea id="textContent" rows="10" cols="60">${collectionContent}</textarea><br>
                                    <button onclick="submitAndClose('${fileType}', ${index}, document.getElementById('textContent').value, null);">Submit</button>
                                </body>
                            </html>
                        `);
                    });
            }
        }, 100); // Add a small delay to ensure the popup is fully loaded
    };
}

function submitAndClose(fileType, index, textContent, deckName) {
    window.opener.submitText(fileType, index, textContent, deckName);
    window.close(); // Close the popup window
}
