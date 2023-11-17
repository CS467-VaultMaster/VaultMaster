import React, { useState } from "react";
import axios from "axios";

function AddCredential({ onAdd }) {
  const [nickname, setNickname] = useState("Amazon");
  const [url, setUrl] = useState("amazon.ca");
  const [password, setPassword] = useState("password");
  const [category, setCategory] = useState("shopping");
  const [note, setNote] = useState("sample note");

  const handleSubmit = async () => {
    try {
      const token = sessionStorage.getItem("authToken");
      if (!token) {
        console.error("No authentication token found.");
        return;
      }

      const response = await axios.post(
        `${process.env.REACT_APP_FASTAPI_URL}/vaultmaster/credential/`,
        {
          nickname: nickname,
          url: url,
          password: password,
          category: category,
          note: note,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (response.status === 200) {
        onAdd(response.data);
        setNickname("");
        setUrl("");
        setPassword("");
        setCategory("");
        setNote("");
      }
    } catch (error) {
      console.error("Error adding credential:", error);
    }
  };

  return (
    <div>
      <h3>Add Credential</h3>
      <div className="add-credential">
        <div className="label-input">
          <label>
            Nickname
            <input
              type="text"
              value={nickname}
              onChange={(e) => setNickname(e.target.value)}
              required
            />
          </label>
        </div>
        <div className="label-input">
          <label>
            URL
            <input
              type="text"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              required
            />
          </label>
        </div>
        <div className="label-input">
          <label>
            Password
            <input
              type="text"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </label>
        </div>
        <div className="label-input">
          <label>
            Category
            <input
              type="text"
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              required
            />
          </label>
        </div>
        <div className="label-input">
          <label>
            Note
            <input
              type="text"
              placeholder="optional"
              value={note}
              onChange={(e) => setNote(e.target.value)}
            />
          </label>
        </div>
        <button onClick={handleSubmit}>Add</button>
      </div>
    </div>
  );
}

export default AddCredential;
