import React, {useState} from "react";
import axios from 'axios'

export default function CredentialsTable({ credentials, onEditComplete, onDelete }) {
  const [editingId, setEditingId] = useState(null)
  const [editForm, setEditForm] = useState({
    nickname: "",
    category: "",
    url: "",
    password: "",
    note: ""
  });
  
  const handleEdit = (credential) => {
    setEditingId(credential.id);
    setEditForm({
      nickname: credential.nickname,
      category: credential.category,
      url: credential.url,
      password: credential.password,
      note: credential.note
    });
  };

  const handleSave = async (id) => {
    console.log(
      editForm
    )
    try {
      const token = sessionStorage.getItem('authToken')
      await axios.put(`${process.env.REACT_APP_FASTAPI_URL}/vaultmaster/credential/${id}`, 
      editForm, 
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      // onEditComplete(id, editedCredential)
      setEditingId(null)  // Exit editing mode
    } catch (error) {
      console.error('Error updating credential:', error)
    }
  }

  const handleChange = (e, field) => {
    setEditForm({
      ...editForm,
      [field]: e.target.value
    });
  };

  return (
    <div className="table-container">
      <h3>Credentials</h3>
      {credentials.length > 0 ? (
        <table className="table">
          <thead>
            <tr>
              <th>Nickname</th>
              <th>URL</th>
              <th>Password</th>
              <th>Category</th>
              <th>Note</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
          {credentials.map((credential) => {
            const isEditing = editingId === credential.id;
            return (
              <tr key={credential.id}>
                {/* Editable fields */}
                {isEditing ? (
                  <>
                    <td><input type="text" value={editForm.nickname} onChange={(e) => handleChange(e, 'nickname')} /></td>
                    <td><input type="text" value={editForm.url} onChange={(e) => handleChange(e, 'url')} /></td>
                    <td>
                      <input type="text" value={editForm.password} onChange={(e) => handleChange(e, 'password')} />
                    </td>
                    <td><input type="text" value={editForm.category} onChange={(e) => handleChange(e, 'category')} /></td>
                    <td><input type="text" value={editForm.note} onChange={(e) => handleChange(e, 'note')} /></td>
                  </>
                ) : (
                  // Non-editable display
                  <>
                    <td>{credential.nickname}</td>
                    <td>{credential.url}</td>
                    <td>{credential.password}</td>
                    <td>{credential.category}</td>
                    <td>{credential.note}</td>
                  </>
                )}

                {/* Action buttons */}
                <td>
                  {isEditing ? (
                    <button onClick={() => handleSave(credential.id)}>Save</button>
                  ) : (
                    <button onClick={() => handleEdit(credential)}>Edit</button>
                  )}
                  <button onClick={() => onDelete(credential.id)}>Delete</button>
                </td>
              </tr>
            );
          })}
        </tbody>
        </table>
      ) : (
        <p>No credentials found.</p>
      )}
    </div>
  );
}
