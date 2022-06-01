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

	return (
		<Layout.Header>
			<Menu theme="dark" mode="horizontal" onClick={onClick} selectedKeys={[]}>
				<Menu.Item key="home" icon={<HomeFilled />}>
					<Link to="/">Home</Link>
				</Menu.Item>
				<Menu.Item key="admin" icon={<SettingFilled />}>
					<a href="/admin/">Admin</a>
				</Menu.Item>
				{authTokens && (
					<Menu.Item
						style={{ marginLeft: "auto" }}
						key="logout"
						icon={<LogoutOutlined />}
					>
						<Link to="/">Logout</Link>
					</Menu.Item>
				)}
			</Menu>
		</Layout.Header>
	);
};

export default Header;
