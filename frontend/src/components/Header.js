import React, { useContext } from "react";
import { Link } from "react-router-dom";
import { Layout, Menu, Tooltip } from "antd";
import {
	HomeFilled,
	UserOutlined,
	SettingFilled,
	LogoutOutlined,
} from "@ant-design/icons";
import AuthContext from "../context/AuthContext";

const Header = ({ newUser }) => {
	let { authTokens, logoutUser } = useContext(AuthContext);

	const onClick = (e) => {
		if (e.key === "logout") {
			logoutUser();
		}
	};

	const items = [
		{
			label: <Link to="/">Home</Link>,
			key: "home",
			icon: <HomeFilled />,
		},
		{
			label: (
				<Link to="/profile/">
					<Tooltip
						title="Complete your member profile."
						placement="bottomRight"
						visible={newUser}
						color="#eb2f96cf"
					>
						Profile
					</Tooltip>
				</Link>
			),
			key: "profile",
			icon: <UserOutlined />,
		},
		{
			label: <a href="/admin/">Admin</a>,
			key: "admin",
			icon: <SettingFilled />,
		},
		authTokens && {
			label: <Link to="/">Logout</Link>,
			key: "logout",
			icon: <LogoutOutlined />,
			style: { marginLeft: "auto" },
		},
	];

	return (
		<Layout.Header>
			<Menu
				items={items}
				theme="dark"
				mode="horizontal"
				onClick={onClick}
				selectedKeys={[]}
			></Menu>
		</Layout.Header>
	);
};

export default Header;
