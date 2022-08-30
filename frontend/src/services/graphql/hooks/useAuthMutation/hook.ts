import {DocumentNode, MutationHookOptions, useMutation} from "@apollo/client";
import {useContext} from "react";
import {AuthContext} from "../../../../context/AuthContext";

export const useAuthMutation = (query: DocumentNode, args: MutationHookOptions) => {
    const {client} = useContext(AuthContext);
    return useMutation(query, {...args, client: client});
};
