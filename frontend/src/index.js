import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import { BrowserRouter } from "react-router-dom";
import { setContext } from "@apollo/client/link/context";
import {
	ApolloClient,
	InMemoryCache,
	createHttpLink,
	ApolloProvider,
} from "@apollo/client";
import { AUTH_TOKEN } from "./constants";

const httpLink = createHttpLink({
	uri: "http://localhost:8000/graphql/",
});

const authLink = setContext((_, { headers }) => {
	const token = localStorage.getItem(AUTH_TOKEN);
	return {
		headers: {
			...headers,
			authorization: token ? `JWT ${token}` : "",
		},
	};
});

const client = new ApolloClient({
	link: authLink.concat(httpLink),
	cache: new InMemoryCache(),
});

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
	<React.StrictMode>
		<BrowserRouter>
			<ApolloProvider client={client}>
				<App />
			</ApolloProvider>
		</BrowserRouter>
	</React.StrictMode>
);
