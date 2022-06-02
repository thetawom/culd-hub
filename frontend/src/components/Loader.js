import { Spin } from "antd";
import React from "react";

const Loader = () => {
	return (
		<Spin
			style={{
				position: "absolute",
				top: "50vh",
				left: "50vw",
				transform: "translate(-50%, -50%)",
			}}
			size="large"
		/>
	);
};

export default Loader;
