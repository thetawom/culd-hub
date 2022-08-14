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

export const UserProvider = ({children}) => {
    let {logoutUser} = useContext(AuthContext);

    let [user, setUser] = useState(null);

    let [isNewUser, setNewUser] = useState(false);

    const checkIsNewUser = (user) => {
        return !user.phone || !user.member.school || !user.member.classYear;
    }

    let {loading} = useAuthQuery(GET_ME_QUERY, {
        onCompleted: ({me}) => {
            setUser(me);
            setNewUser(checkIsNewUser(me));
        },
        onError: () => logoutUser(),
    });

    let contextData = {
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
}
