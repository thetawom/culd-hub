import { createContext, useEffect, useState } from "react";
import {
	ApolloClient,
	createHttpLink,
	gql,
	InMemoryCache,
	useMutation,
} from "@apollo/client";
import { setContext } from "@apollo/client/link/context";
import { useNavigate } from "react-router-dom";
import jwt_decode from "jwt-decode";
import dayjs from "dayjs";
import { AUTH_TOKEN, REFRESH_TOKEN } from "../constants";

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

export const REFRESH_TOKEN_MUTATION = gql`
	mutation RefreshToken($refreshToken: String!) {
		refreshToken(refreshToken: $refreshToken) {
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

	let [client, setClient] = useState(null);

	let [refreshToken] = useMutation(REFRESH_TOKEN_MUTATION, {
		onCompleted: ({ refreshToken }) => {
			setAuthTokens({
				access: refreshToken.token,
				refresh: refreshToken.refreshToken,
			});
			localStorage.setItem(AUTH_TOKEN, refreshToken.token);
			localStorage.setItem(REFRESH_TOKEN, refreshToken.refreshToken);
		},
		onError: (error) => {
			console.log(error.message);
			setAuthTokens(null);
			localStorage.removeItem(AUTH_TOKEN);
			localStorage.removeItem(REFRESH_TOKEN);
		},
	});

	useEffect(() => {
		if (authTokens) {
			const httpLink = createHttpLink({
				uri: "http://localhost:8000/graphql/",
			});

			const authLink = setContext((_, { headers }) => {
				const exp = jwt_decode(authTokens.access).exp;
				const isExpired = dayjs.unix(exp).diff(dayjs()) < 1;

				if (isExpired) {
					refreshToken({
						variables: {
							refreshToken: authTokens.refresh,
						},
					});
				}

				return {
					headers: {
						...headers,
						authorization: authTokens ? `JWT ${authTokens.access}` : "",
					},
				};
			});

			setClient(
				new ApolloClient({
					link: authLink.concat(httpLink),
					cache: new InMemoryCache(),
				})
			);
		} else {
			setClient(null);
		}
	}, [authTokens]);

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
		client: client,
		loginUser: loginUser,
		logoutUser: logoutUser,
	};

	return (
		<AuthContext.Provider value={contextData}>{children}</AuthContext.Provider>
	);
};
