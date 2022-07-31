import {useLazyQuery} from "@apollo/client";
import {useContext} from "react";
import AuthContext from "../context/AuthContext";

const useAuthLazyQuery = (query, args) => {
    const {client} = useContext(AuthContext);
    return useLazyQuery(query, {...args, client: client});
};

export default useAuthLazyQuery;
