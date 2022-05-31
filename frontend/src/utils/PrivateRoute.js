import { useContext } from "react";
import { Navigate } from "react-router-dom";
import AuthContext from "../context/AuthContext";

const PrivateRoute = ({ children }) => {
	let { authTokens } = useContext(AuthContext);
	return authTokens ? children : <Navigate to="/login" />;
};

export default PrivateRoute;
