import React from "react";
import {Divider, Image, Typography} from "antd";
import logo from "../assets/logo.png";

interface Props {
    title?: string,
    subtitle?: React.ReactNode,
    alert?: React.ReactNode,
    children?: React.ReactNode,
}

const AuthBox: React.FC<Props> = ({title, subtitle, alert, children}) => {
    return (
        <div
            style={{
                width: "100vw",
                height: "100vh",
                backgroundColor: "#F8F8F8",
            }}
        >
            <div
                style={{
                    width: "80%",
                    maxWidth: "400px",
                    minWidth: "300px",
                    backgroundColor: "white",
                    padding: "30px",
                    paddingBottom: "15px",
                    borderRadius: "5px",
                    position: "absolute",
                    left: "50%",
                    top: "50%",
                    transform: "translate(-50%, -55%)",
                }}
            >
                <div
                    style={{
                        textAlign: "center",
                        marginTop: "10px",
                        marginBottom: "20px",
                    }}
                >
                    <Image
                        width={150}
                        src={logo}
                        style={{
                            borderRadius: "20px",
                        }}
                        preview={false}
                    />
                </div>
                <Typography.Title
                    level={1}
                    style={{textAlign: "center", marginBottom: "0.2em"}}
                >
                    {title ? title : "CU Lion Dance"}
                </Typography.Title>
                <Typography style={{textAlign: "center", marginBottom: "1em"}}>
                    {subtitle}
                </Typography>
                {alert}
                <Divider style={{marginTop: "6px"}}/>
                {children}
            </div>
        </div>
    );
};

export default AuthBox;
