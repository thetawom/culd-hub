import {DocumentNode, QueryHookOptions, useQuery} from "@apollo/client";
import {useContext} from "react";
import AuthContext from "../../context/AuthContext";

const useAuthQuery = (query: DocumentNode, args: QueryHookOptions) => {
    const {client} = useContext(AuthContext);
    return useQuery(query, {...args, client: client});
};

export default useAuthQuery;
