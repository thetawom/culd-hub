import React, {createContext, useContext, useState} from "react";
import Loader from "../../components/Loader";
import {useAuthQuery} from "../../services/graphql/";
import {AuthContext} from "../AuthContext";
import {GET_ME_QUERY} from "./constants";
import {User} from "./types";

export const UserContext = createContext(undefined);

interface Props {
    children: React.ReactNode[],
}

export const UserProvider: React.FC<Props> = ({children}: Props) => {
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
