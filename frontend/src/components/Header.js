import React, { useContext } from "react";
import { Link } from "react-router-dom";
import { Layout, Menu } from "antd";
import { HomeFilled, SettingFilled, LogoutOutlined } from "@ant-design/icons";
import AuthContext from "../context/AuthContext";

const Header = () => {
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
