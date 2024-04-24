import React, { useState } from 'react';
import { TextField, Button, Grid, Paper } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const Register = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    const user = { username, email, password };

    try {
      const response = await fetch('http://localhost:5000/api/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(user),
      });

      if (!response.ok) {
        throw new Error('Failed to register');
      }

      alert('Registration successful!');
      navigate('/login'); // Redirect to login page after registration
    } catch (error) {
      alert(error.message);
    }
  };

  return (
    <Paper sx={{ p: 2, backgroundColor: '#121212', color: '#fff' }}> {/* Dark background and light text */}
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
                    borderColor: '#468AD7', 
                    borderWidth: '1px', 
                  },
                  '&:hover fieldset': {
                    borderColor: '#00B4FD',
                  },
                }
              }}
              InputLabelProps={{
                style: { color: '#fff' } // Light labels for better visibility
              }}
              inputProps={{
                style: { color: '#fff' } // Light text for inputs
              }}
            />
          </Grid>
          <Grid item xs={12}>
            <TextField 
              fullWidth 
              label="Email" 
              variant="outlined" 
              value={email} 
              onChange={(e) => setEmail(e.target.value)}
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
              Register
            </Button>
          </Grid>
        </Grid>
      </form>
    </Paper>
  );
};

export default Register;
