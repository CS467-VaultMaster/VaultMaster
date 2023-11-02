import React from "react";

export default function CredentialsTable() {
  return (
    <div>
      <h3>Credentials</h3>
      {credentials.length > 0 ? (
        <table>
          <thead>
            <tr>
              <th>Nickname</th>
              <th>URL</th>
              <th>Password</th>
              <th>Category</th>
            </tr>
          </thead>
          <tbody>
            {credentials.map((credential, index) => (
              <tr key={index}>
                <td>{credential.nickname}</td>
                <td>{credential.url}</td>
                <td>{credential.password}</td>
                <td>{credential.category}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No credentials found.</p>
      )}
    </div>
  );
}
