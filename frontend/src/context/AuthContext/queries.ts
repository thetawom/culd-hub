import {gql} from "@apollo/client";

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
            success
            errors
        }
    }
`;