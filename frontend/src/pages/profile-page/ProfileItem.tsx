import React, {useState} from "react";
import {Button, Card, Form, Input, message} from "antd";
import {CheckOutlined, EditTwoTone} from "@ant-design/icons";
import styles from "./ProfileItem.module.css";
import {APIInterface, handleApolloError, useAuthMutation} from "../../services/graphql";
import {User} from "../../context/UserContext";
import {gql} from "@apollo/client";

const UPDATE_PROFILE_MUTATION = gql`
    mutation UpdateProfile (
        $email: String
        $firstName: String
        $lastName: String
        $phone: String
        $classYear: String
        $school: String
    ) {
        updateProfile (
            email: $email
            firstName: $firstName
            lastName: $lastName
            phone: $phone
            classYear: $classYear
            school: $school
        ) {
            success
            errors
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
    choices?: StringDict,
}

type UpdateProfileType = APIInterface & {
    user: User;
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

    const [editUser] = useAuthMutation(UPDATE_PROFILE_MUTATION, {
        onCompleted: async ({updateProfile}: { updateProfile: UpdateProfileType }) => {
            if (updateProfile.success) {
                setEditing(false);
                await message.success(`Successfully edited your ${title.toLowerCase()}`);
            } else {
                const errors = updateProfile.errors;
                await message.error(errors[Object.keys(errors)[0]][0].message);
            }
        },
        onError: handleApolloError(() => {
            setEditing(false);
        }),
    });

    const onSubmit = async (formValues: StringDict) => {
        let modified = false;
        for (const prop in formValues) {
            if (formValues[prop] !== values[prop]) {
                modified = true;
                break;
            }
        }
        if (modified) {
            await editUser({variables: formValues});
        } else {
            setEditing(false);
        }
    };

    return (<Card
        hoverable
        onClick={() => {
            if (!editing) {
                setEditing(true);
            }
        }}
    >
        <div className={styles.content}>
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
