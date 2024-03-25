import React, { useEffect, useState } from 'react';
import {useNavigate} from "react-router-dom";

const UserLogin = (props) => {
  const [user, setUser] = useState('')
  const [password, setPassword] = useState('')
  const [userError, setUserError] = useState('')
  const [passwordError, setPasswordError] = useState('')

  const navigate = useNavigate()

  const onButtonClick = () => {
     setUserError('')
     setPasswordError('')
     if ('' === password) {
        setPasswordError('Please enter your CISE Oracle Database password')
        return
     }
  }

  return (
    <div className={'mainContainer'}>
      <div className={'titleContainer'}>
        <div>Login</div>
      </div>
      <br />
      <div className={'inputContainer'}>
        <input
          value={user}
          placeholder="Enter your username here"
          onChange={(ev) => setUser(ev.target.value)}
          className={'inputBox'}
        />
        <label className="errorLabel">{userError}</label>
      </div>
      <br />
      <div className={'inputContainer'}>
        <input
          value={password}
          placeholder="Enter your password here"
          onChange={(ev) => setPassword(ev.target.value)}
          className={'inputBox'}
        />
        <label className="errorLabel">{passwordError}</label>
      </div>
      <br />
      <div className={'inputContainer'}>
        <input className={'inputButton'} type="button" onClick={onButtonClick} value={'Log in'} />
      </div>
    </div>
  )
}

export default UserLogin
