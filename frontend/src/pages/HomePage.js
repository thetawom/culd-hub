import React, { useContext } from "react";
import { Divider, Layout, Typography } from "antd";
import { AppstoreAddOutlined } from "@ant-design/icons";
import UserContext from "../context/UserContext";
import Header from "../components/Header";
import ShowsTable from "../components/ShowsTable";
import { ShowsTableProvider } from "../context/ShowsTableContext";
import ShowsTableControls from "../components/ShowsTableControls";

const HomePage = () => {
	let { user } = useContext(UserContext);

	return (
		<Layout style={{ minHeight: "100vh" }}>
			<Header newUser={!user.member.school || !user.member.classYear} />
			<Layout.Content
				style={{
					width: "90%",
					margin: "auto",
					padding: "30px",
				}}
			>
				<ShowsTableProvider>
					<div style={{ display: "flex", justifyContent: "space-between" }}>
						<Typography.Title level={2} style={{ marginBottom: "0em" }}>
							<AppstoreAddOutlined
								style={{
									fontSize: "0.9em",
									marginRight: "0.4em",
								}}
							/>
							Performance Sign-ups
						</Typography.Title>
						<ShowsTableControls />
					</div>
					<Divider style={{ marginTop: "1em", marginBottom: "1.4em" }} />
					<ShowsTable user={user} />
				</ShowsTableProvider>
			</Layout.Content>
		</Layout>
	);
};

export default HomePage;
