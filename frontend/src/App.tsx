import "./App.css";
import React from "react";
import {Route, Routes} from "react-router-dom";
import ShowsPage from "./pages/ShowsPage";
import ProfilePage from "./pages/ProfilePage";
import PrivateRoutes from "./components/PrivateRoutes";
import {AuthProvider} from "./context/AuthContext";
import {message, Spin} from "antd";
import Loader from "./components/Loader";
import {ForgotPasswordPage, LoginPage, ResetPasswordPage, SignupPage} from "./pages/AuthPages";


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
                        <Route path="/" element={<ShowsPage/>}/>
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
