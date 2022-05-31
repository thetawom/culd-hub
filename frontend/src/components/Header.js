import React, { useContext } from "react";
import { Link } from "react-router-dom";
import AuthContext from "../context/AuthContext";

const Header = () => {
	let { authTokens, logoutUser } = useContext(AuthContext);
	return (
		<div>
			<Link to="/">Home</Link>
			<span> | </span>
			{authTokens ? (
				<span onClick={logoutUser}>Logout</span>
			) : (
				<Link to="/login">Login</Link>
			)}
			{authTokens && <p>Hello!</p>}
		</div>
	);
};

export default Header;
