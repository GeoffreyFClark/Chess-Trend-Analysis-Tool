import { createTheme } from '@mui/material/styles';

// https://mui.com/material-ui/customization/theming/
const theme = createTheme({
  palette: {
    mode: 'light',
  },
  components: {
    MuiOutlinedInput: {
      styleOverrides: {
        root: {
          height: '40px', 
        },
      },
    },
  },
});

export default theme;
