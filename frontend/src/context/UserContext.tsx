import {gql} from "@apollo/client";
import React, {createContext, useContext, useState} from "react";
import Loader from "../components/Loader";
import useAuthQuery from "../utils/hooks/useAuthQuery";
import AuthContext from "./AuthContext";
import PropTypes from "prop-types";

const UserContext = createContext(undefined);

export default UserContext;

const GET_ME_QUERY = gql`
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

interface Props {
    children: React.ReactNode,
}

class User {
    phone: string;
    member: Member;
}

class Member {
    school: string;
    classYear: string;
}

export const UserProvider: React.FC<Props> = ({children}) => {
    const {logoutUser} = useContext(AuthContext);

    const [user, setUser] = useState(null);

    const [isNewUser, setNewUser] = useState(false);

    const checkIsNewUser = (user: User) => {
        return !user.phone || !user.member.school || !user.member.classYear;
    };

    const {loading} = useAuthQuery(GET_ME_QUERY, {
        onCompleted: ({me}: { me: User }) => {
            setUser(me);
            setNewUser(checkIsNewUser(me));
        },
        onError: () => logoutUser(),
    });

    const contextData = {
        user: user,
        isNewUser: isNewUser,
    };

    return (
        <UserContext.Provider value={contextData}>
            {loading || !user ? <Loader/> : <>{children}</>}
        </UserContext.Provider>
    );
};

UserProvider.propTypes = {
    children: PropTypes.element,
};
