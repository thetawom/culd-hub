import { gql } from "@apollo/client";
import React, { useContext, useState } from "react";
import { Layout } from "antd";
import AuthContext from "../context/AuthContext";
import useAuthQuery from "../utils/useAuthQuery";
import Header from "../components/Header";
import Loader from "../components/Loader";

const GET_ME_QUERY = gql`
	{
		me {
			id
			firstName
			lastName
			member {
				school
				classYear
			}
		}
	}
`;

const ProfilePage = () => {
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
			<Header
				newUser={!loading && (!user?.member.school || !user?.member.classYear)}
			/>
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
					<div>{`This is ${user.firstName}'s profile page.`}</div>
				)}
			</Layout.Content>
		</Layout>
	);
};

export default ProfilePage;
