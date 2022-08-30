import {gql} from "@apollo/client";

export const RESET_PASSWORD_MUTATION = gql`
    mutation ResetPassword (
        $userId: ID!
        $token: String!
        $password: String!
    ) {
        resetPassword(
            userId: $userId
            token: $token
            password: $password
        ) {
            success
            errors
        }
    }
`;