import {gql} from "@apollo/client";

export const GET_SHOWS_QUERY = gql`
	{
		shows {
			id
			name
			priority
			date
			time
			rounds {
				id
				time
			}
			address
			lions
			performers {
				user {
					id
					firstName
					lastName
				}
			}
			point {
				user {
					id
					firstName
					lastName
				}
			}
			contact {
				firstName
				lastName
				phone
				email
			}
			isCampus
			isOutOfCity
			isOpen
			isPending
			status
			notes
		}
	}
`;

export const CREATE_ROLE_MUTATION = gql`
	mutation CreateRole($showId: ID!) {
		createRole(showId: $showId) {
			role {
				show {
					id
					name
				}
				performer {
					user {
						id
						firstName
						lastName
					}
				}
			}
		}
	}
`;

export const DELETE_ROLE_MUTATION = gql`
	mutation DeleteRole($showId: ID!) {
		deleteRole(showId: $showId) {
			role {
				show {
					id
					name
				}
				performer {
					user {
						id
					}
				}
			}
		}
	}
`;

export const GET_SHOW_PRIORITY_CHOICES_QUERY = gql`
	{
		showPriorityChoices
	}
`;

export const GET_SHOW_STATUS_CHOICES_QUERY = gql`
	{
		showStatusChoices
	}
`;