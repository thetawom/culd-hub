import { gql } from "@apollo/client";
import React, { createContext, useContext, useState } from "react";
import Loader from "../components/Loader";
import useAuthQuery from "../utils/useAuthQuery";
import AuthContext from "./AuthContext";

const UserContext = createContext();

export default UserContext;

const GET_ME_QUERY = gql`
	{
		me {
			id
			firstName
			lastName
			member {
				school
				classYear
			}
		}
	}
`;

export const UserProvider = ({ children }) => {
	let { logoutUser } = useContext(AuthContext);

	let [user, setUser] = useState(null);

	let { loading } = useAuthQuery(GET_ME_QUERY, {
		onCompleted: ({ me }) => {
			setUser(me);
		},
		onError: () => logoutUser(),
	});

	let contextData = {
		user: user,
	};

	return (
		<UserContext.Provider value={contextData}>
			{loading ? <Loader /> : <>{children}</>}
		</UserContext.Provider>
	);
};
