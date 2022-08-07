import {useMutation} from "@apollo/client";
import {useContext} from "react";
import AuthContext from "../../context/AuthContext";

const useAuthMutation = (query, args) => {
    const {client} = useContext(AuthContext);
    return useMutation(query, {...args, client: client});
};

export default useAuthMutation;
