import {Spin} from "antd";
import {LoadingOutlined} from "@ant-design/icons";
import React from "react";

const Loader = () => {
    return (
        <Spin className={"spin"}
              indicator={<LoadingOutlined spin/>}
        />
    );
};

export default Loader;
