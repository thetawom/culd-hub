import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import {BrowserRouter} from "react-router-dom";
import {
    ApolloClient, InMemoryCache, createHttpLink, ApolloProvider,
} from "@apollo/client";

const client = new ApolloClient({
    link: createHttpLink({
        uri: "/graphql/",
    }), cache: new InMemoryCache(),
});

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<React.StrictMode>
    <BrowserRouter>
        <ApolloProvider client={client}>
            <App/>
        </ApolloProvider>
    </BrowserRouter>
</React.StrictMode>);
