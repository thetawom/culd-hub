import "./App.css";
import React from "react";
import {Route, Routes} from "react-router-dom";
import ShowsPage from "./pages/ShowsPage";
import ProfilePage from "./pages/ProfilePage";
import PrivateRoutes from "./components/PrivateRoutes";
import {AuthProvider} from "./context/AuthContext";
import {message} from "antd";
import {
    ForgotPasswordPage,
    LoginPage,
    ResetPasswordPage,
    SignupPage
} from "./pages/AuthPages";


function App() {
    message.config({
        duration: 1.5,
    });

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
                    <Route path="password_reset/"
                           element={<ForgotPasswordPage/>}/>
                    <Route path="password_reset/:userId/:token/"
                           element={<ResetPasswordPage/>}/>
                </Routes>
            </AuthProvider>
        </div>
    );
}

export default App;
