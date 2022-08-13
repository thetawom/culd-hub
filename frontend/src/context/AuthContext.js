import {createContext, useEffect, useState} from "react";
import {ApolloClient, createHttpLink, gql, InMemoryCache, useMutation,} from "@apollo/client";
import {setContext} from "@apollo/client/link/context";
import {useLocation, useNavigate} from "react-router-dom";
import jwt_decode from "jwt-decode";
import dayjs from "dayjs";
import {AUTH_TOKEN, REFRESH_TOKEN, REMEMBER_EMAIL} from "../constants";
import {message} from "antd";

const AuthContext = createContext(undefined);

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

export const LOGOUT_USER_MUTATION = gql`
    mutation LogoutUser {
        logoutUser {
            ok
        }
    }
`

export const AuthProvider = ({children}) => {
    const navigate = useNavigate();
    const location = useLocation();

    let [invalidCredentials, setInvalidCredentials] = useState(false);

    let [authTokens, setAuthTokens] = useState(() =>
        localStorage.getItem(AUTH_TOKEN) && localStorage.getItem(REFRESH_TOKEN)
            ? {
                access: localStorage.getItem(AUTH_TOKEN),
                refresh: localStorage.getItem(REFRESH_TOKEN),
            }
            : null
    );

    let [client, setClient] = useState(null);

    let [tokenAuth] = useMutation(TOKEN_AUTH_MUTATION, {
        onCompleted: ({tokenAuth}) => {
            setInvalidCredentials(false);
            setAuthTokens({
                access: tokenAuth.token,
                refresh: tokenAuth.refreshToken,
            });
            localStorage.setItem(AUTH_TOKEN, tokenAuth.token);
            localStorage.setItem(REFRESH_TOKEN, tokenAuth.refreshToken);
            navigate(location.state?.from || "/");
        },
        onError: (error) => {
            if (error.message === "Please enter valid credentials") {
                console.log(error.message);
                setInvalidCredentials(true);
            } else {
                message.error(error.message);
            }
        },
    });

    let [logoutUserMutation] = useMutation(LOGOUT_USER_MUTATION);

    let loginUser = ({email, password}) => {
        localStorage.setItem(REMEMBER_EMAIL, email);
        tokenAuth({
            variables: {
                email: email,
                password: password,
            },
        });
    };

    let logoutUser = () => {
        setAuthTokens(null);
        localStorage.removeItem(AUTH_TOKEN);
        localStorage.removeItem(REFRESH_TOKEN);
        logoutUserMutation();
        navigate("/login");
    };

    let [refreshToken] = useMutation(REFRESH_TOKEN_MUTATION, {
        onCompleted: ({refreshToken}) => {
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
                uri: "/graphql/",
            });

            const authLink = setContext(async (_, {headers}) => {
                const exp = jwt_decode(authTokens.access).exp;
                const isExpired = dayjs.unix(exp).diff(dayjs()) < 1;

                if (isExpired) {
                    await refreshToken({
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
    }, [authTokens, refreshToken]);

    let contextData = {
        authTokens: authTokens,
        client: client,
        invalidCredentials: invalidCredentials,
        loginUser: loginUser,
        logoutUser: logoutUser,
        setInvalidCredentials: setInvalidCredentials,
    };

    return (
        <AuthContext.Provider value={contextData}>{children}</AuthContext.Provider>
    );
};
