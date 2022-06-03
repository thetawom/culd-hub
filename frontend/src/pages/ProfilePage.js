import React, { useContext } from "react";
import { Layout, Typography } from "antd";
import UserContext from "../context/UserContext";
import Header from "../components/Header";

const ProfilePage = () => {
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
				<Typography.Title level={2} style={{ marginBottom: "0em" }}>
					{`Welcome, ${user.firstName}!`}
				</Typography.Title>
			</Layout.Content>
		</Layout>
	);
};

export default ProfilePage;
