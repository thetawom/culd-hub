import {gql} from "@apollo/client";

export const GET_SCHOOL_CHOICES_QUERY = gql`
	{
		schoolChoices
	}
`;

export const GET_CLASS_YEAR_CHOICES_QUERY = gql`
	{
		classYearChoices
	}
`;

export const GET_POSITION_CHOICES_QUERY = gql`
    {
        positionChoices
    }
`;

export const UPDATE_PROFILE_MUTATION = gql`
    mutation UpdateProfile (
        $email: String
        $firstName: String
        $lastName: String
        $phone: String
        $classYear: String
        $school: String
    ) {
        updateProfile (
            email: $email
            firstName: $firstName
            lastName: $lastName
            phone: $phone
            classYear: $classYear
            school: $school
        ) {
            success
            errors
            user {
                id
                firstName
                lastName
                email
                phone
                member {
                    id
                    classYear
                    school
                }
            }
        }
    }
`;

export const UPDATE_PASSWORD_MUTATION = gql`
    mutation UpdateProfile (
        $oldPassword: String
        $password: String
    ) {
        updatePassword (
            oldPassword: $oldPassword
            password: $password
        ) {
            success
            errors
        }
    }
`;