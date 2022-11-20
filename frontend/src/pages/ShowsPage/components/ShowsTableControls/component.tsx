import React, {useContext} from "react";
import {Button, Segmented, Select, Space, Tooltip} from "antd";
import {SyncOutlined} from "@ant-design/icons";
import ShowsTableContext from "../../context/ShowsTableContext";
import {Options, Views} from "./constants";
import styles from "./style.module.css";

const ShowsTableControls = () => {

    const {view, optionsFilter, setView, setOptionsFilter, setNeedsRefresh} =
        useContext(ShowsTableContext);

    return (
        <Space className={styles.space}>
            <Tooltip title="Refetch shows" placement="bottom">
                <Button onClick={() => setNeedsRefresh(true)}>
                    <SyncOutlined/>
                </Button>
            </Tooltip>
            <Segmented
                options={[Options.OPEN, Options.CLOSED, Options.MINE, Options.ALL]}
                value={optionsFilter}
                onChange={setOptionsFilter}
                onResize={undefined}
                onResizeCapture={undefined}/>
            <Select
                value={view}
                onChange={setView}
                options={[
                    {
                        value: Views.TABLE,
                        label: "Table",
                    },
                    {
                        value: Views.CALENDAR,
                        label: "Calendar",
                    }
                ]}
            />
        </Space>
    );
};

export default ShowsTableControls;
