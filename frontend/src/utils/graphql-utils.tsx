import {ApolloError} from "@apollo/client";
import {message} from "antd";

export const onApolloError = async (error: ApolloError) => {
    console.log(error.message);
    if (error.networkError) {
        await message.error("Sorry, we encountered a network error.️");
    } else {
        await message.error(error.message);
    }
};