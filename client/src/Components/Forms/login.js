import React from "react";
import { useDispatch } from "react-redux";

// import Button from "@material-ui/core/Button";
import CssBaseline from "@material-ui/core/CssBaseline";
// import TextField from "@material-ui/core/TextField";
// import FormControlLabel from "@material-ui/core/FormControlLabel";
// import Checkbox from "@material-ui/core/Checkbox";
import Link from "@material-ui/core/Link";
// import Grid from "@material-ui/core/Grid";
import Box from "@material-ui/core/Box";

import Typography from "@material-ui/core/Typography";
import { makeStyles } from "@material-ui/core/styles";
import Container from "@material-ui/core/Container";
import { frontURL } from "../../axios";
import NormalLoader from "../Loaders/normalBackdrop";
// import { Link as RouteLink } from "react-router-dom";
import GoogleLogin from "react-google-login";
// import { googleLogin } from "../../store/slices/authSlice";
import { googleLogin } from "../../axios";
import Developers from "./developers";

import LoginPic from "../../assets/login.png";

import "./style.scss";

export function Copyright() {
  return (
    <div>
      <Typography variant="body2" color="textSecondary" align="center">
        {"Copyright © "}
        <Link color="inherit" href={frontURL}>
          NimbusNest
        </Link>{" "}
        {new Date().getFullYear()}
        {"."}
      </Typography>
      <Developers />
    </div>
  );
}

const useStyles = makeStyles((theme) => ({
  paper: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
  },
  avatar: {
    margin: theme.spacing(1),
    backgroundColor: theme.palette.secondary.main,
  },
  form: {
    width: "100%", // Fix IE 11 issue.
    marginTop: theme.spacing(1),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
}));

export default function SignIn(props) {
  const classes = useStyles();

  const dispatch = useDispatch();

  window.localStorage.removeItem("access_token");
  window.localStorage.removeItem("id");

  // let [state, setState] = useState({
  //   username: "",
  //   password: "",
  // });

  // let inputChangeHandler = (e) => {
  //   setState({
  //     ...state,
  //     [e.target.name]: e.target.value,
  //   });
  // };

  // let handleLogin = (e, data) => {
  //   e.preventDefault();
  //   dispatch(loginAsync(data, props));
  // };
  // const googleResponse = ({ profileObj }) => {
  //   //console.log(profileObj);
  //   dispatch(googleLogin(profileObj, props));
  // };

  return (
    <Container
      className="box"
      style={{
        marginTop: "100px",
        padding: "20px",
      }}
      component="main"
      maxWidth="xs"
    >
      <NormalLoader />
      <CssBaseline />
      {/* {//console.log(state)} */}
      <div className={classes.paper}>
        <Typography
          style={{
            fontWeight: "bold",
            textShadow: "1px 1px grey",
            margin: "15px 0",
          }}
          component="h1"
          variant="h4"
        >
          NimbusNest
        </Typography>

        <div style={{ margin: "10px 0", width: "100%" }}>
          <img style={{ width: "100%" }} src={LoginPic} alt="loginpic" />
        </div>

        {/* <form className={classes.form} noValidate>
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            id="username"
            label="Username"
            name="username"
            autoComplete="username"
            autoFocus
            onChange={inputChangeHandler}
          />
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            name="password"
            label="Password"
            type="password"
            id="password"
            onChange={inputChangeHandler}
            autoComplete="current-password"
          />
          <FormControlLabel
            control={<Checkbox value="remember" color="primary" />}
            label="Remember me"
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            color="primary"
            className={classes.submit}
            onClick={(e) => handleLogin(e, state)}
          >
            Sign In
          </Button>
          <Grid container>
            <Grid item xs>
              <Link href="#" variant="body2">
                Forgot password?
              </Link>
            </Grid>
            <Grid item>
              <RouteLink to="/signup" variant="body2">
                {"Don't have an account? Sign Up"}
              </RouteLink>
            </Grid>
          </Grid>
        </form> */}
        <div style={{ marginTop: "20px" }}>
          <GoogleLogin
            clientId="575084088742-2eidkevqutnod9lord9vf2sri50ko7ct.apps.googleusercontent.com"
            buttonText="LOGIN WITH GOOGLE"
            onSuccess={(response) => googleLogin(props, response)(dispatch)}
            render={(renderProps) => (
              <button
                onClick={renderProps.onClick}
                disabled={renderProps.disabled}
                type="button"
                class="login-with-google-btn"
              >
                Sign in with Google
              </button>
            )}
            // onFailure={googleResponse}
          />
        </div>
      </div>
      <Box mt={8}>
        <Copyright />
      </Box>
    </Container>
  );
}
