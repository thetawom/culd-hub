import "./App.css";
import React from "react";
import {Route, Routes} from "react-router-dom";
import ShowsPage from "./pages/shows-page/ShowsPage";
import ProfilePage from "./pages/profile-page/ProfilePage";
import LoginPage from "./pages/auth-pages/LoginPage";
import SignupPage from "./pages/auth-pages/SignupPage";
import PrivateRoutes from "./utils/PrivateRoutes";
import {AuthProvider} from "./context/AuthContext";
import {message} from "antd";
import ForgotPasswordPage from "./pages/auth-pages/ForgotPasswordPage";
import ResetPasswordPage from "./pages/auth-pages/ResetPasswordPage";

function App() {
    message.config({
        duration: 1.5,
    });

    return (<div className="App">
        <AuthProvider>
            <Routes>
                <Route element={<PrivateRoutes/>}>
                    <Route path="/" exact element={<ShowsPage/>}/>
                    <Route path="profile/" element={<ProfilePage/>}/>
                </Route>
                <Route path="login/" element={<LoginPage/>}/>
                <Route path="signup/" element={<SignupPage/>}/>
                <Route path="password_reset/" element={<ForgotPasswordPage/>}/>
                <Route path="password_reset/:userId/:token" element={<ResetPasswordPage/>}/>
            </Routes>
        </AuthProvider>
    </div>);
}

export default App;
