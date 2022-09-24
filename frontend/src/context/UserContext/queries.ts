import {gql} from "@apollo/client";

export const GET_ME_QUERY = gql`
	{
		me {
			id
			firstName
			lastName
			member {
			    id
			    position
				school
				classYear
			}
			email
			phone
		}
	}
`;