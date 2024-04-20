import React from 'react';
import { AppBar, Toolbar, Typography, Button, IconButton, Box } from '@mui/material';
// import MenuIcon from '@mui/icons-material/Menu';
import { Link } from 'react-router-dom';

function Navigation() {
  return (
    <>
    <AppBar position="static">
      <Toolbar style={{ minHeight: '56px' }}>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          Chess Opening Database Project
        </Typography>
        <Button color="inherit" component={Link} sx={{ '&:hover': { color: 'white', bgcolor: 'rgba(255, 255, 255, 0.2)' } }} to="/">Home</Button>
        <Button color="inherit" component={Link} sx={{ '&:hover': { color: 'white', bgcolor: 'rgba(255, 255, 255, 0.2)' } }} to="/query-openings">Query Openings</Button>
        <Button color="inherit" component={Link} sx={{ '&:hover': { color: 'white', bgcolor: 'rgba(255, 255, 255, 0.2)' } }} to="/query-results">Results</Button>
      </Toolbar>
    </AppBar>
    <Box mt={4}> 
    </Box>
    </>
  );
}

export default Navigation;
