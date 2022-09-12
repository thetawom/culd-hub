import {Spin} from "antd";
import React from "react";
import {LoadingOutlined} from "@ant-design/icons";
import styles from "./style.module.css";

const Loader = () => {
    return (
        <Spin
            className={styles.spin}
            indicator={<LoadingOutlined spin/>}
            size="large"
        />
    );
};

export default Loader;
