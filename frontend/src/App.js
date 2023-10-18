import React, { useState, useEffect } from 'react';

function App() {
    const [items, setItems] = useState([]);

    useEffect(() => {
        console.log("Starting the fetch operation...");
    
        fetch(`${process.env.REACT_APP_FASTAPI_URL}/items/`)
            .then(response => {
                console.log("Received the response:", response);
                return response.json();
            })
            .then(data => {
                console.log("Parsed JSON data:", data);
                setItems(data);
            })
            .catch(error => {
                console.error("Error during the fetch operation:", error);
            });
    }, []);
    

    return (
        <div className="App">
            <h1>Items</h1>
            <ul>
                {items.map(item => (
                    <li key={item.id}>{item.name}</li>
                ))}
            </ul>
        </div>
    );
}

export default App;

