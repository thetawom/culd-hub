import React, {createContext, useEffect, useState} from "react";
import {handleApolloError, useMutation} from "../../services/graphql";
import {useLocation, useNavigate} from "react-router-dom";
import jwt_decode from "jwt-decode";
import dayjs from "dayjs";
import {AUTH_TOKEN, REFRESH_TOKEN, REMEMBER_EMAIL,} from "./constants";
import {
    LOGOUT_USER_MUTATION,
    REFRESH_TOKEN_MUTATION,
    TOKEN_AUTH_MUTATION
} from "./queries";
import {
    ApolloClient,
    ApolloError,
    createHttpLink,
    InMemoryCache
} from "@apollo/client";
import {setContext} from "@apollo/client/link/context";

export const AuthContext = createContext(undefined);

interface Props {
    children: React.ReactNode
}

export const AuthProvider: React.FC<Props> = ({children}: Props) => {

    const navigate = useNavigate();
    const location = useLocation();

    const [invalidCredentials, setInvalidCredentials] = useState(false);
    const [inactiveUser, setInactiveUser] = useState(false);

    const [authTokens, setAuthTokens] = useState(() =>
        localStorage.getItem(AUTH_TOKEN) && localStorage.getItem(REFRESH_TOKEN)
            ? {
                access: localStorage.getItem(AUTH_TOKEN),
                refresh: localStorage.getItem(REFRESH_TOKEN),
            }
            : null
    );

    const [client, setClient] = useState(null);

    const [tokenAuth] = useMutation(TOKEN_AUTH_MUTATION, {
        onCompleted: ({tokenAuth}) => {
            setInvalidCredentials(false);
            setAuthTokens({
                access: tokenAuth.token,
                refresh: tokenAuth.refreshToken,
            });
            localStorage.setItem(AUTH_TOKEN, tokenAuth.token);
            localStorage.setItem(REFRESH_TOKEN, tokenAuth.refreshToken);
            const state = location.state as { from: string; };
            navigate(state?.from || "/");
        },
        onError: handleApolloError((error: ApolloError) => {
            if (error.message === "Please enter valid credentials") {
                setInvalidCredentials(true);
                return true;
            } else if (error.message === "User is not active") {
                setInactiveUser(true);
                return true;
            }
        }),
    });

    const [logoutUserMutation] = useMutation(LOGOUT_USER_MUTATION);

    interface LoginType {
        email: string,
        password: string
    }

    const loginUser = async ({email, password}: LoginType) => {
        localStorage.setItem(REMEMBER_EMAIL, email);
        await tokenAuth({
            variables: {
                email: email,
                password: password,
            },
        });
    };

    const logoutUser = async () => {
        await logoutUserMutation();
        setAuthTokens(null);
        localStorage.removeItem(AUTH_TOKEN);
        localStorage.removeItem(REFRESH_TOKEN);
        navigate("/login");
    };

    const [refreshToken] = useMutation(REFRESH_TOKEN_MUTATION, {
        onCompleted: ({refreshToken}) => {
            setAuthTokens({
                access: refreshToken.token,
                refresh: refreshToken.refreshToken,
            });
            localStorage.setItem(AUTH_TOKEN, refreshToken.token);
            localStorage.setItem(REFRESH_TOKEN, refreshToken.refreshToken);
        },
        onError: (error) => {
            console.error(error.message);
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

                type TokenType = { exp: number; }
                const exp = jwt_decode<TokenType>(authTokens.access).exp;
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

    const contextData = {
        authTokens: authTokens,
        client: client,
        invalidCredentials: invalidCredentials,
        inactiveUser: inactiveUser,
        loginUser: loginUser,
        logoutUser: logoutUser,
        setInvalidCredentials: setInvalidCredentials,
        setInactiveUser: setInactiveUser,
    };

    return (
        <AuthContext.Provider value={contextData}>
            {children}
        </AuthContext.Provider>
    );
};