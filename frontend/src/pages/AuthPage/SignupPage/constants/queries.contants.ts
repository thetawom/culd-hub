import {gql} from "@apollo/client";

export const REGISTER_MUTATION = gql`
	mutation Register(
		$email: String!
		$password1: String!
		$password2: String!
		$firstName: String!
		$lastName: String!
		$phone: String!
	) {
		register(
			email: $email
			password1: $password1
			password2: $password2
			firstName: $firstName
			lastName: $lastName
			phone: $phone
		) {
		    success
		    errors
			user {
				id
				firstName
				lastName
				email
				phone
			}
		}
	}
`;