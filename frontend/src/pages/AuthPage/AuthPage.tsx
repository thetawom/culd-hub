import React from "react";
import {Divider, Image, Typography} from "antd";
import logo from "../../assets/logo.png";
import styles from "./AuthPage.module.css";

interface Props {
    title?: string,
    subtitle?: React.ReactNode,
    alert?: React.ReactNode,
    children?: React.ReactNode,
}

const AuthPage: React.FC<Props> = ({title, subtitle, alert, children}) => {
    return (
        <div className={styles.background}>
            <div className={styles.panel}>
                <div className={styles.logo}>
                    <Image width={150} src={logo} preview={false}/>
                </div>
                <Typography.Title level={1} className={styles.title}>
                    {title ? title : "CU Lion Dance"}
                </Typography.Title>
                <Typography className={styles.subtitle}>
                    {subtitle}
                </Typography>
                {alert}
                <Divider className={styles.divider}/>
                {children}
            </div>
        </div>
    );
};

export default AuthPage;
