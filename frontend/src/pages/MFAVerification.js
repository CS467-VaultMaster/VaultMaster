import React from 'react'
import {useNavigate} from 'react-router-dom'

export default function MFAVerification({setIsAuthenticated}) {
  const navigate = useNavigate()

  const handleClick = () => {
    setIsAuthenticated(true)
    navigate('/vault')
  }

  return (
    <div className="mfa-page">
      <h2>MFA Confirmation</h2>
      <button onClick={handleClick}>MFA Good</button>
    </div>
  )
}
