import { gql } from "@apollo/client";
import React, { useContext, useState } from "react";
import { Switch, Divider, Layout, Spin, Typography, Space } from "antd";
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
			setUser(me);
		},
		onError: () => logoutUser(),
	});

	let [showClosed, setShowClosed] = useState(false);

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
						<Space>
							<Typography.Title level={2} style={{ marginBottom: "0.3em" }}>
								{`Welcome, ${user.firstName}!`}
							</Typography.Title>
							<Switch
								checkedChildren="Hide"
								unCheckedChildren="Show"
								defaultChecked
								style={{ marginLeft: "10px" }}
								onClick={(checked) => setShowClosed(!checked)}
							/>
						</Space>
						<Divider style={{ marginTop: "0.2", marginBottom: "1.2em" }} />
						<ShowsTable user={user} showClosed={showClosed} />
					</>
				)}
			</Layout.Content>
		</Layout>
	);
};

export default HomePage;
