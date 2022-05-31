import { gql } from "@apollo/client";
import React, { useContext, useState } from "react";
import AuthContext from "../context/AuthContext";
import useAuthQuery from "../utils/useAuthQuery";
import Header from "../components/Header";

const GET_SHOWS_QUERY = gql`
	{
		shows {
			id
			name
			date
		}
	}
`;

const HomePage = () => {
	let { logoutUser } = useContext(AuthContext);
	let [shows, setShows] = useState([]);

	let { loading } = useAuthQuery(GET_SHOWS_QUERY, {
		onCompleted: ({ shows }) => {
			console.log(shows);
			setShows(shows);
		},
		onError: () => logoutUser(),
	});

	return loading ? (
		<p>Loading ...</p>
	) : (
		<>
			<Header />
			<div>
				{shows.map(({ id, name, date }) => (
					<p key={id}>
						{name} {date}
					</p>
				))}
			</div>
		</>
	);
};

export default HomePage;
