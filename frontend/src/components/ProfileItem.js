import React, {useState} from "react";
import {Button, Card, Input} from "antd";
import {CheckOutlined, EditTwoTone} from "@ant-design/icons";
import { gql } from "@apollo/client";
import { Mutation } from '@apollo/react-components';

const EDIT_USER = gql`
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
    console.log("Title: " + title, "Value: " + value, "Choices: " + choices)

    return (
        <Mutation mutation={EDIT_USER}>
            {editUser => (
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
                                choices ? choices[value] ?? value : value
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
            )}
            
        </Mutation>
    );
};

export default ProfileItem;
