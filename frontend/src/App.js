import "./App.css";
import React from "react";
import {Route, Routes} from "react-router-dom";
import {ForgotPasswordPage, LoginPage, ResetPasswordPage, SignupPage} from "./pages/AuthPage";
import ShowsPage from "./pages/shows-page/ShowsPage";
import ProfilePage from "./pages/profile-page/ProfilePage";
import PrivateRoutes from "./components/PrivateRoutes";
import {AuthProvider} from "./context/AuthContext";
import {message, Spin} from "antd";
import Loader from "./components/Loader";


function App() {
    message.config({
        duration: 1.5,
    });

    Spin.setDefaultIndicator(<Loader/>);

    return (
        <div className="App">
            <AuthProvider>
                <Routes>
                    <Route element={<PrivateRoutes/>}>
                        <Route path="/" exact element={<ShowsPage/>}/>
                        <Route path="profile/" element={<ProfilePage/>}/>
                    </Route>
                    <Route path="login/" element={<LoginPage/>}/>
                    <Route path="signup/" element={<SignupPage/>}/>
                    <Route path="password_reset/" element={<ForgotPasswordPage/>}/>
                    <Route path="password_reset/:userId/:token/"
                           element={<ResetPasswordPage/>}/>
                </Routes>
            </AuthProvider>
        </div>
    );
}

export default App;
