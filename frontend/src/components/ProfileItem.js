import React, {useState} from "react";
import {Button, Card, Input} from "antd";
import {CheckOutlined, EditTwoTone} from "@ant-design/icons";

const ProfileItem = ({title, value, input, choices}) => {
    let [editing, setEditing] = useState(false);

    return (
        <Card
            hoverable
            onClick={() => {
                if (!editing) {
                    setEditing(true);
                }
            }}
        >
            <div
                style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                }}
            >
                <Card.Meta
                    title={title}
                    description={
                        editing ? (
                            <Input.Group compact style={{width: "100%"}}>
                                {input}
                                <Button
                                    type="primary"
                                    style={{width: "50px"}}
                                    onClick={() => {
                                        setEditing(false);
                                    }}
                                >
                                    <CheckOutlined/>
                                </Button>
                            </Input.Group>
                        ) : (
                            choices ? choices[value] : value
                        )
                    }
                    style={{width: "100%"}}
                />
                {!editing && (
                    <EditTwoTone
                        style={{
                            fontSize: "1.8em",
                        }}
                    />
                )}
            </div>
        </Card>
    );
};

export default ProfileItem;
