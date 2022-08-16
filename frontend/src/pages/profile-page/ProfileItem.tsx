import React, {useState} from "react";
import {Button, Card, Form, Input, message} from "antd";
import {CheckOutlined, EditTwoTone} from "@ant-design/icons";
import {gql} from "@apollo/client";
import useAuthMutation from "../../utils/hooks/useAuthMutation";

const EDIT_USER_MUTATION = gql`
    mutation EditUser (
        $email: String
        $firstName: String
        $lastName: String
        $phone: String
        $classYear: String
        $school: String
    ) {
        editUser (
            email: $email
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
                    id
                    classYear
                    school
                }
            }
        }
    }
`;

type StringDict = { [index: string]: string }

interface Props {
    title: string,
    values: StringDict,
    display: (values: StringDict) => string,
    input: React.ReactNode,
    choices: StringDict,
}

const ProfileItem: React.FC<Props> = ({
                                          title,
                                          values,
                                          display,
                                          input,
                                          choices
                                      }) => {
    const [form] = Form.useForm();

    const [editing, setEditing] = useState(false);

    const [editUser] = useAuthMutation(EDIT_USER_MUTATION, {
        onCompleted: async () => {
            await message.success(`Successfully edited your ${title.toLowerCase()}`);
        }, onError: (error) => {
            console.log(error.message);
        },
    });

    const onSubmit = (formValues: StringDict) => {
        let modified = false;
        for (const prop in formValues) {
            if (formValues[prop] !== values[prop]) {
                modified = true;
                break;
            }
        }
        if (modified) {
            editUser({variables: formValues});
        }
        setEditing(false);
    };

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
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
            }}
        >
            <Card.Meta
                title={title}
                description={editing ? (<Form form={form} onFinish={onSubmit}
                                              style={{width: "100%"}}>
                    <Input.Group compact style={{width: "100%"}}>
                        {input}
                        <Form.Item shouldUpdate noStyle>
                            {() => <Button type="primary" htmlType="submit"
                                           style={{width: "50px"}}
                                           disabled={!!form.getFieldsError().filter(({errors}) => errors.length).length}>
                                <CheckOutlined/>
                            </Button>}
                        </Form.Item>
                    </Input.Group>
                </Form>) : (choices ? choices[display(values)] ?? display(values) : display(values))}
                style={{width: "100%"}}
            />
            {!editing && (<EditTwoTone
                style={{
                    fontSize: "1.8em",
                }}
            />)}
        </div>
    </Card>);
};

export default ProfileItem;
