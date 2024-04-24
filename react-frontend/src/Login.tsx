import React, { useState } from 'react';
import { TextField, Button, Grid, Paper } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    const user = { username, password };
    try {
      const response = await fetch('http://localhost:5000/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(user),
      });
      if (!response.ok) {
        throw new Error('Login failed');
      }
      const data = await response.json();
      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('username', username);
      alert('Login successful!');
      navigate('/query-openings');
    } catch (error) {
      alert(error.message);
    }
  };

  return (
    <Paper sx={{ p: 2 }}>
      <form onSubmit={handleSubmit}>
        <Grid container alignItems="flex-start" spacing={2}>
          <Grid item xs={12}>
            <TextField fullWidth label="Username" variant="outlined" value={username} onChange={(e) => setUsername(e.target.value)} />
          </Grid>
          <Grid item xs={12}>
            <TextField fullWidth label="Password" type="password" variant="outlined" value={password} onChange={(e) => setPassword(e.target.value)} />
          </Grid>
          <Grid item xs={12}>
            <Button type="submit" variant="contained" color="primary" fullWidth>
              Login
            </Button>
          </Grid>
        </Grid>
      </form>
    </Paper>
  );
};

export default Login;
