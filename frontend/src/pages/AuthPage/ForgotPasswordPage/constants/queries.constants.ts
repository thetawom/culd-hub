import {gql} from "@apollo/client";

export const SEND_PASSWORD_RESET_EMAIL_MUTATION = gql`
    mutation SendPasswordResetEmail ($email: String!) {
        sendPasswordResetEmail(email: $email) {
            success
            errors
        }
    }
`;