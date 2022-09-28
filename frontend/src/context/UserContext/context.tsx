import React, {createContext, useContext, useState} from "react";
import Loader from "../../components/Loader";
import {QueryResult, useAuthQuery} from "../../services/graphql/";
import {AuthContext} from "../AuthContext";
import {GET_ME_QUERY} from "./queries";
import {User} from "../../types/types";

export const UserContext = createContext(undefined);

interface Props {
    children: React.ReactNode[],
}

export const UserProvider: React.FC<Props> = ({children}: Props) => {
    const {logoutUser} = useContext(AuthContext);

    const [user, setUser] = useState(null);

    const [isNewUser, setNewUser] = useState(false);

    const checkIsNewUser = (user: User) => {
        return !user.phone || user.member.school == null || user.member.classYear == null;
    };

    const {loading}: QueryResult = useAuthQuery(GET_ME_QUERY, {
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
