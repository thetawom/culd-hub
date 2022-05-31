import { createContext, useState } from "react";
import { gql, useMutation } from "@apollo/client";
import { AUTH_TOKEN, REFRESH_TOKEN } from "../constants";
import { useNavigate } from "react-router-dom";

const AuthContext = createContext();

export default AuthContext;

export const TOKEN_AUTH_MUTATION = gql`
	mutation TokenAuth($email: String!, $password: String!) {
		tokenAuth(email: $email, password: $password) {
			token
			payload
			refreshToken
			refreshExpiresIn
		}
	}
`;

export const AuthProvider = ({ children }) => {
	let [authTokens, setAuthTokens] = useState(() =>
		localStorage.getItem(AUTH_TOKEN)
			? {
					access: localStorage.getItem(AUTH_TOKEN),
					refresh: localStorage.getItem(REFRESH_TOKEN),
			  }
			: null
	);

	const navigate = useNavigate();

	let [tokenAuth] = useMutation(TOKEN_AUTH_MUTATION, {
		onCompleted: ({ tokenAuth }) => {
			setAuthTokens({
				access: tokenAuth.token,
				refresh: tokenAuth.refreshToken,
			});
			localStorage.setItem(AUTH_TOKEN, tokenAuth.token);
			localStorage.setItem(REFRESH_TOKEN, tokenAuth.refreshToken);
			navigate("/");
		},
		onError: (error) => {
			if (error.message === "Please enter valid credentials") {
				console.log(error.message);
			} else {
				alert(error.message);
			}
		},
	});
	let loginUser = (e) => {
		e.preventDefault();
		tokenAuth({
			variables: {
				email: e.target.email.value,
				password: e.target.password.value,
			},
		});
	};

	let logoutUser = () => {
		setAuthTokens(null);
		localStorage.removeItem(AUTH_TOKEN);
		localStorage.removeItem(REFRESH_TOKEN);
		navigate("/login");
	};

	let contextData = {
		authTokens: authTokens,
		loginUser: loginUser,
		logoutUser: logoutUser,
	};

	return (
		<AuthContext.Provider value={contextData}>{children}</AuthContext.Provider>
	);
};
