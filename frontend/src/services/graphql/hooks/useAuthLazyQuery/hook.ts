import {DocumentNode, LazyQueryHookOptions, useLazyQuery} from "@apollo/client";
import {useContext} from "react";
import {AuthContext} from "../../../../context/AuthContext";

export const useAuthLazyQuery = (query: DocumentNode, args: LazyQueryHookOptions) => {
    const {client} = useContext(AuthContext);
    return useLazyQuery(query, {...args, client: client});
};
