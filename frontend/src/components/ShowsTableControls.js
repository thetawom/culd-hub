import React, { useContext } from "react";
import { Segmented, Button, Space, Tooltip } from "antd";
import { SyncOutlined } from "@ant-design/icons";
import ShowsTableContext from "../context/ShowsTableContext";

const ShowsTableControls = () => {
	let { openFilter, setOpenFilter, setNeedsRefresh } =
		useContext(ShowsTableContext);

	return (
		<Space style={{ marginTop: "auto" }}>
			<Tooltip title="Refetch shows" placement="bottom">
				<Button onClick={() => setNeedsRefresh(true)}>
					<SyncOutlined />
				</Button>
			</Tooltip>
			<Segmented
				options={["Open", "Closed", "All"]}
				value={openFilter}
				onChange={setOpenFilter}
			/>
		</Space>
	);
};

export default ShowsTableControls;
