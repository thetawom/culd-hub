import React, {useState} from "react";
import {Button, Card, Form, Input, message} from "antd";
import {CheckOutlined, EditTwoTone} from "@ant-design/icons";
import styles from "./style.module.css";
import {
    APIInterface,
    handleApolloError,
    useAuthMutation
} from "../../../../services/graphql";
import {UPDATE_PROFILE_MUTATION} from "../../queries";
import {User} from "../../../../types/types";


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
                                      }: Props) => {
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
            if (values[prop] != formValues[prop]) {
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

    if (editing) {
        return <Card hoverable>
            <div className={styles.content}>
                <Card.Meta title={title}/>
            </div>
            <Form form={form} onFinish={onSubmit}>
                <Input.Group compact>
                    {input}
                    <Form.Item shouldUpdate noStyle>
                        {() =>
                            <Button type="primary"
                                    htmlType="submit"
                                    className={styles.submitButton}
                                    disabled={!!form.getFieldsError().filter(({errors}) => errors.length).length}>
                                <CheckOutlined/>
                            </Button>}
                    </Form.Item>
                </Input.Group>
            </Form>
        </Card>;
    } else {
        return <Card hoverable onClick={() => setEditing(true)}>
            <div className={styles.content}>
                <Card.Meta title={title}
                           description={(choices ? choices[display(values)] ?? display(values) : display(values))}/>
                <EditTwoTone className={styles.editButton}/>
            </div>
        </Card>;
    }
};

export default ProfileItem;
