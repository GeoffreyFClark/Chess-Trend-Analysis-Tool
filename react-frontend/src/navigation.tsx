import { React, useState }  from 'react';
import { AppBar, Toolbar, Typography, Button, IconButton, Box, Menu, MenuItem, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle } from '@mui/material';
import { Link, useNavigate } from 'react-router-dom';

function Navigation() {
  const navigate = useNavigate();
  const username = localStorage.getItem('username');
  const [anchorEl, setAnchorEl] = useState(null);
  const [contactDialogOpen, setContactDialogOpen] = useState(false);


  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    setAnchorEl(null); 
    navigate('/login');
  };

  const handleMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleContactClick = () => {
    setContactDialogOpen(true);
  };

  const handleContactDialogClose = () => {
    setContactDialogOpen(false);
  };

  const buttonHoverStyle = { '&:hover': { color: 'white', bgcolor: 'rgba(255, 255, 255, 0.2)' } }

  return (
    <>
    <AppBar position="static">
      <Toolbar style={{ minHeight: '56px' }}>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          Chess Trends Analyzer
        </Typography>
        {username ? (
          <Box sx={{ position: 'relative', display: 'inline-block' }}>
            <Button color="inherit" component={Link} sx={buttonHoverStyle} to="/query-openings">Query Openings</Button>
            <Button color="inherit" component={Link} sx={buttonHoverStyle} to="/query-results">Results</Button>
            <Button
              color="inherit"
              aria-controls="user-menu"
              aria-haspopup="true"
              onClick={handleMenuOpen}
              sx={buttonHoverStyle}
            >
              {username}
            </Button>
            <Menu
              id="user-menu"
              anchorEl={anchorEl}
              open={Boolean(anchorEl)}
              onClose={handleMenuClose}
              anchorOrigin={{
                vertical: 'bottom',
                horizontal: 'right',
              }}
              transformOrigin={{
                vertical: 'top',
                horizontal: 'right',
              }}
            >
              <MenuItem onClick={handleLogout}>Logout</MenuItem>
            </Menu>
          </Box>
        ) : (
          <>
            <Button color="inherit" component={Link} to="/login" sx={buttonHoverStyle}>
              Login
            </Button>
            <Button color="inherit" component={Link} to="/register" sx={buttonHoverStyle}>
              Register
            </Button>
          </>
        )}
        <Button color="inherit" onClick={handleContactClick} sx={buttonHoverStyle}>
          Contact Us
        </Button>
        <Dialog open={contactDialogOpen} onClose={handleContactDialogClose}>
          <DialogTitle>Contact Information</DialogTitle>
          <DialogContent>
            <DialogContentText>
              For any questions or feedback, please contact us at:
              <br />
              Email: Support@ChessDBproject.com
              <br />
              Phone: (352) 618-3749
            </DialogContentText>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleContactDialogClose} color="primary">
              Close
            </Button>
          </DialogActions>
        </Dialog>
      </Toolbar>
    </AppBar>
    <Box mt={4}> 
    </Box>
    </>
  );
}

export default Navigation;
