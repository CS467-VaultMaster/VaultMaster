import React, {useState} from 'react'

export default function GeneratePassword() {
    const [generatedPassword, setGeneratedPassword] = useState('')

    const generatePassword = () => {
        const charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*(){}[],./;':"
        let password = ""
        for (let i=0; i < 16; i++){
            password += charset.charAt(Math.floor(Math.random() * charset.length))
        }
        setGeneratedPassword(password)
    }

  return (
    <div>
      <button type="button" onClick={generatePassword}>
        Generate Strong Password
      </button>
      {generatedPassword && (
        <div className="generated-password">
          Generated Password: {generatedPassword}
        </div>
      )}
    </div>
  )
}
