import { gql } from "@apollo/client";
import React, { useContext, useState } from "react";
import {
	Divider,
	Layout,
	Typography,
	Segmented,
	Button,
	Space,
	Tooltip,
} from "antd";
import { SyncOutlined } from "@ant-design/icons";
import AuthContext from "../context/AuthContext";
import useAuthQuery from "../utils/useAuthQuery";
import Header from "../components/Header";
import ShowsTable from "../components/ShowsTable";
import Loader from "../components/Loader";

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

	let [openFilter, setOpenFilter] = useState("Open");

	let [refreshed, setRefreshed] = useState(false);

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
					<>
						<div style={{ display: "flex", justifyContent: "space-between" }}>
							<Typography.Title level={2} style={{ marginBottom: "0em" }}>
								{`Welcome, ${user.firstName}!`}
							</Typography.Title>
							<Space style={{ marginTop: "auto" }}>
								<Tooltip title="Refetch shows" placement="bottom">
									<Button onClick={() => setRefreshed(false)}>
										<SyncOutlined />
									</Button>
								</Tooltip>
								<Segmented
									options={["Open", "Closed", "All"]}
									value={openFilter}
									onChange={setOpenFilter}
								/>
							</Space>
						</div>
						<Divider style={{ marginTop: "0.8em", marginBottom: "1.2em" }} />
						<ShowsTable
							user={user}
							openFilter={openFilter}
							refreshed={refreshed}
							setRefreshed={setRefreshed}
						/>
					</>
				)}
			</Layout.Content>
		</Layout>
	);
};

export default HomePage;
