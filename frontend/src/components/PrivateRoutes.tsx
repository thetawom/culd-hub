import React, {useContext} from "react";
import {Navigate, Outlet, useLocation} from "react-router-dom";
import {AuthContext} from "../context/AuthContext";
import {UserProvider} from "../context/UserContext";

const PrivateRoutes = () => {
    const location = useLocation();
    const {authTokens} = useContext(AuthContext);

    return authTokens ? (
        <UserProvider>
            <Outlet/>{" "}
        </UserProvider>
    ) : (
        <Navigate to="/login" replace state={{from: location}}/>
    );
};

export default PrivateRoutes;
