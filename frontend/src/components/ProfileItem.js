import React, {useState} from "react";
import {Button, Card, Form, Input} from "antd";
import {CheckOutlined, EditTwoTone} from "@ant-design/icons";
import {gql} from "@apollo/client";

const EDIT_USER_MUTATION = gql`
  mutation EditUser (
    $email: String!
    $firstName: String!
    $lastName: String!
    $phone: String!
    $classYear: String!
    $school: String!
    ) {
    editUser(email: $email
        firstName: $firstName
        lastName: $lastName
        phone: $phone
        classYear: $classYear
        school: $school
    ) {
        user {
            id
            firstName
            lastName
            email
            phone
            member {
                classYear
                school
            }
        }
    }
  }
`;

const ProfileItem = ({title, value, input, choices}) => {
    let [editing, setEditing] = useState(false);

    const onSubmit = (values) => {
        setEditing(false);
        console.log("Setting", values);
    }

    return (<Card
        hoverable
        onClick={() => {
            if (!editing) {
                setEditing(true);
            }
        }}
    >
        <div
            style={{
                display: "flex", justifyContent: "space-between", alignItems: "center",
            }}
        >
            <Card.Meta
                title={title}
                description={editing ? (<Form onFinish={onSubmit} style={{width: "100%"}}>
                    <Input.Group compact style={{width: "100%"}}>
                        {input}
                        <Form.Item noStyle>
                            <Button type="primary" htmlType="submit" style={{width: "50px"}}>
                                <CheckOutlined/>
                            </Button>
                        </Form.Item>
                    </Input.Group>
                </Form>) : (choices ? choices[value] ?? value : value)}
                style={{width: "100%"}}
            />
            {!editing && (<EditTwoTone
                style={{
                    fontSize: "1.8em",
                }}
            />)}
        </div>
    </Card>);
}


export default ProfileItem;
