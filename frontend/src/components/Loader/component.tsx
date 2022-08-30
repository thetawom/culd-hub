import {Spin} from "antd";
import {LoadingOutlined} from "@ant-design/icons";
import React from "react";
import styles from "./style.module.css";

const Loader = () => {
    return (
        <Spin className={styles.spin}
              indicator={<LoadingOutlined spin/>}
        />
    );
};

export default Loader;
