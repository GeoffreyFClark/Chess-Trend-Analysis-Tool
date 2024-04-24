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
    <Paper sx={{ p: 2, backgroundColor: '#121212', color: '#fff' }}>
      <form onSubmit={handleSubmit}>
        <Grid container alignItems="flex-start" spacing={2}>
          <Grid item xs={12}>
            <TextField 
              fullWidth 
              label="Username" 
              variant="outlined" 
              value={username} 
              onChange={(e) => setUsername(e.target.value)}
              sx={{
                '& .MuiOutlinedInput-root': {
                  '& fieldset': {
                    borderColor: '#468AD7', // Change to any color that makes it more visible
                    borderWidth: '1px', // Makes the border thicker and more visible
                  },
                  '&:hover fieldset': {
                    borderColor: '#00B4FD', // Changes border color on hover
                  },
                }
              }}
              InputLabelProps={{
                style: { color: '#fff' }
              }}
              inputProps={{
                style: { color: '#fff' }
              }}
            />
          </Grid>
          <Grid item xs={12}>
            <TextField 
              fullWidth 
              label="Password" 
              type="password" 
              variant="outlined" 
              value={password} 
              onChange={(e) => setPassword(e.target.value)}
              sx={{
                '& .MuiOutlinedInput-root': {
                  '& fieldset': {
                    borderColor: '#468AD7', 
                    borderWidth: '1px', 
                  },
                  '&:hover fieldset': {
                    borderColor: '#00B4FD',
                  },
                }
              }}
              InputLabelProps={{
                style: { color: '#fff' }
              }}
              inputProps={{
                style: { color: '#fff' }
              }}
            />
          </Grid>
          <Grid item xs={12}>
            <Button type="submit" variant="contained" color="primary" fullWidth style={{ backgroundColor: '#1976d2', color: '#fff' }}>
              Login
            </Button>
          </Grid>
        </Grid>
      </form>
    </Paper>
  );
};

export default Login;