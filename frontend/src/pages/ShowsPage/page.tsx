import React, {useContext} from "react";
import {Divider, Layout, Row, Typography} from "antd";
import {AppstoreAddOutlined} from "@ant-design/icons";
import {UserContext} from "../../context/UserContext";
import Header from "../../components/Header";
import ShowsTable from "./components/ShowsTable";
import {ShowsTableProvider} from "./context/ShowsTableContext";
import {User} from "../../types/types";
import styles from "./style.module.css";
import ShowsTableControls from "./components/ShowsTableControls";

const ShowsPage = () => {

    const {user}: { user: User } = useContext(UserContext);

    return (
        <Layout>
            <Header newUserTooltip/>
            <Layout.Content className={styles.content}>
                <ShowsTableProvider>
                    <Row justify="space-between" align="bottom"
                         className={styles.heading}>
                        <Typography.Title className={styles.title} level={2}>
                            <AppstoreAddOutlined className={styles.icon}/>
                            Performance Sign-ups
                        </Typography.Title>
                        <ShowsTableControls/>
                    </Row>
                    <Divider className={styles.divider}/>
                    <ShowsTable user={user}/>
                </ShowsTableProvider>
            </Layout.Content>
        </Layout>
    );
};

export default ShowsPage;
