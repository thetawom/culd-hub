import React, {useContext} from "react";
import {Link} from "react-router-dom";
import {Layout, Menu, Tooltip} from "antd";
import {HomeFilled, LogoutOutlined, SettingFilled, SmileOutlined,} from "@ant-design/icons";
import AuthContext from "../context/AuthContext";
import UserContext from "../context/UserContext";
import styles from "./Header.module.css";

interface Props {
    newUserTooltip?: boolean,
}

const Header: React.FC<Props> = ({newUserTooltip}) => {
    const {authTokens, logoutUser} = useContext(AuthContext);

    const {user, isNewUser} = useContext(UserContext);

    const onClick = (e) => {
        if (e.key === "logout") {
            logoutUser();
        }
    };

    const items = [
        {
            label: <Link to="/">Home</Link>,
            key: "home",
            icon: <HomeFilled/>,
        },
        {
            label: <a href="/admin/">Admin</a>,
            key: "admin",
            icon: <SettingFilled/>,
        },
        user && {
            label: (
                <Link to="/profile/">
                    <Tooltip
                        title="Complete your member profile"
                        placement="bottomRight"
                        visible={newUserTooltip && isNewUser}
                        color="#eb2f96"
                        overlayClassName={styles.tooltip}
                    >
                        {user.firstName} {user.lastName}
                    </Tooltip>
                </Link>
            ),
            key: "profile",
            icon: <SmileOutlined/>,
            style: {marginLeft: "auto"},
        },
        authTokens && {
            label: <Link to="/">Logout</Link>,
            key: "logout",
            icon: <LogoutOutlined/>,
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
