import { useContext } from "react";
import { Navigate, Outlet } from "react-router-dom";
import AuthContext from "../context/AuthContext";
import { UserProvider } from "../context/UserContext";

const PrivateRoutes = () => {
	let { authTokens } = useContext(AuthContext);
	return authTokens ? (
		<UserProvider>
			<Outlet />{" "}
		</UserProvider>
	) : (
		<Navigate to="/login" />
	);
};

export default PrivateRoutes;
