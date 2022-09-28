import React, {useContext} from "react";
import {Button, Segmented, Space, Tooltip} from "antd";
import {SyncOutlined} from "@ant-design/icons";
import ShowsTableContext from "../../context/ShowsTableContext";
import {OPTIONS_ENUM} from "./constants";
import styles from "./style.module.css";

const ShowsTableControls = () => {

    const {openFilter, setOpenFilter, setNeedsRefresh} =
        useContext(ShowsTableContext);

    return (
        <Space className={styles.space}>
            <Tooltip title="Refetch shows" placement="bottom">
                <Button onClick={() => setNeedsRefresh(true)}>
                    <SyncOutlined/>
                </Button>
            </Tooltip>
            <Segmented
                options={[OPTIONS_ENUM.OPEN, OPTIONS_ENUM.CLOSED, OPTIONS_ENUM.MINE, OPTIONS_ENUM.ALL]}
                value={openFilter}
                onChange={setOpenFilter}
            />
        </Space>
    );
};

export default ShowsTableControls;
