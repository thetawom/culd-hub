import {ApolloError} from "@apollo/client";
import {message} from "antd";

export const handleApolloError = (handler: (error: ApolloError) => void | boolean = undefined) => {
    return async (error: ApolloError) => {
        console.error(error.message);
        let handled: void | boolean = false;
        if (handler !== undefined) {
            handled = handler(error);
        }
        if (!handled) {
            if (error.networkError) {
                await message.error("Sorry, we encountered a network error.️");
            } else {
                await message.error(error.message);
            }
        }
    };
};