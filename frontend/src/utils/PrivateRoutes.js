import { useContext } from "react";
import { Navigate, Outlet } from "react-router-dom";
import AuthContext from "../context/AuthContext";

const PrivateRoutes = () => {
	let { authTokens } = useContext(AuthContext);
	return authTokens ? <Outlet /> : <Navigate to="/login" />;
};

export default PrivateRoutes;
