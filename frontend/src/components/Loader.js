import {Spin} from "antd";
import {LoadingOutlined} from "@ant-design/icons";
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
            indicator={
                <LoadingOutlined
                    style={{
                        fontSize: 60,
                    }}
                    spin
                />
            }
        />
    );
};

export default Loader;
