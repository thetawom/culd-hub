import React, {useContext} from "react";
import {Button, Segmented, Space, Tooltip} from "antd";
import {SyncOutlined} from "@ant-design/icons";
import ShowsTableContext from "./ShowsTableContext";

export const OPTIONS_ENUM = {
    OPEN: "Open",
    CLOSED: "Closed",
    MINE: "Mine",
    ALL: "All"
};

Object.freeze(OPTIONS_ENUM);

const ShowsTableControls = () => {
    let {openFilter, setOpenFilter, setNeedsRefresh} =
        useContext(ShowsTableContext);

    return (
        <Space style={{marginTop: "auto"}}>
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
