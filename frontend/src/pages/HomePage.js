import { gql } from "@apollo/client";
import React, { useContext, useState } from "react";
import { Divider, Layout, Typography } from "antd";
import AuthContext from "../context/AuthContext";
import useAuthQuery from "../utils/useAuthQuery";
import Header from "../components/Header";
import ShowsTable from "../components/ShowsTable";
import Loader from "../components/Loader";
import { ShowsTableProvider } from "../context/ShowsTableContext";
import ShowsTableControls from "../components/ShowsTableControls";

const GET_ME_QUERY = gql`
	{
		me {
			id
			firstName
			lastName
		}
	}
`;

const HomePage = () => {
	let { logoutUser } = useContext(AuthContext);

	let [user, setUser] = useState(null);

	let { loading } = useAuthQuery(GET_ME_QUERY, {
		onCompleted: ({ me }) => {
			setUser(me);
		},
		onError: () => logoutUser(),
	});

	return (
		<Layout style={{ minHeight: "100vh" }}>
			<Header />
			<Layout.Content
				style={{
					width: "90%",
					margin: "auto",
					padding: "30px",
				}}
			>
				{loading ? (
					<Loader />
				) : (
					<ShowsTableProvider>
						<div style={{ display: "flex", justifyContent: "space-between" }}>
							<Typography.Title level={2} style={{ marginBottom: "0em" }}>
								{`Welcome, ${user.firstName}!`}
							</Typography.Title>
							<ShowsTableControls />
						</div>
						<Divider style={{ marginTop: "0.8em", marginBottom: "1.2em" }} />
						<ShowsTable user={user} />
					</ShowsTableProvider>
				)}
			</Layout.Content>
		</Layout>
	);
};

export default HomePage;
