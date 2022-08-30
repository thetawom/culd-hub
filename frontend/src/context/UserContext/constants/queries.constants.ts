import {gql} from "@apollo/client";

export const GET_ME_QUERY = gql`
	{
		me {
			id
			firstName
			lastName
			member {
			    id
				school
				classYear
				membership
			}
			email
			phone
		}
	}
`;