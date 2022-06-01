import { gql } from "@apollo/client";
import React, { useContext, useState } from "react";
import { Divider, Layout, Spin, Typography } from "antd";
import AuthContext from "../context/AuthContext";
import useAuthQuery from "../utils/useAuthQuery";
import Header from "../components/Header";
import ShowsTable from "../components/ShowsTable";

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
			console.log(me);
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
					<Spin
						style={{
							position: "absolute",
							top: "50vh",
							left: "50vw",
							transform: "translate(-50%, -50%)",
						}}
						size="large"
					/>
				) : (
					<>
						<Typography.Title level={2} style={{ marginBottom: "0.3em" }}>
							{`Welcome, ${user.firstName}!`}
						</Typography.Title>
						<Divider style={{ marginTop: "1.5em", marginBottom: "2em" }} />
						<ShowsTable user={user} />
					</>
				)}
			</Layout.Content>
		</Layout>
	);
};

export default HomePage;
