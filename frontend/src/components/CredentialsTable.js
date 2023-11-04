import React, {useState} from "react";
import axios from 'axios'

export default function CredentialsTable({ credentials, onEditComplete, onDelete }) {
  const [editingId, setEditingId] = useState(null)
  const [editedCredential, setEditedCredential] = useState({})
  
  const handleEdit = (credential) => {
    setEditingId(credential.id)
    setEditedCredential({...credential})  // Clone credential to edit
  }

  const handleSave = async (id) => {
    try {
      const token = sessionStorage.getItem('authToken')
      await axios.put(`${process.env.REACT_APP_FASTAPI_URL}/vaultmaster/credential/${id}`, editedCredential, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      onEditComplete(id, editedCredential)
      setEditingId(null)  // Exit editing mode
    } catch (error) {
      console.error('Error updating credential:', error)
    }
  }

  const handleChange = (e, field) => {
    setEditedCredential({
      ...editedCredential,
      [field]: e.target.value
    })
  }

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
                    <td><input type="text" value={editedCredential.nickname} onChange={(e) => handleChange(e, 'nickname')} /></td>
                    <td><input type="text" value={editedCredential.url} onChange={(e) => handleChange(e, 'url')} /></td>
                    <td>
                      <input type="password" value={editedCredential.password} onChange={(e) => handleChange(e, 'password')} />
                    </td>
                    <td><input type="text" value={editedCredential.category} onChange={(e) => handleChange(e, 'category')} /></td>
                    <td><input type="text" value={editedCredential.note} onChange={(e) => handleChange(e, 'note')} /></td>
                  </>
                ) : (
                  // Non-editable display
                  <>
                    <td>{credential.nickname}</td>
                    <td>{credential.url}</td>
                    <td>{'•'.repeat(credential.password.length)}</td>
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
