import React, {useState} from "react";
import {Button, Card, Form, Input, message} from "antd";
import {EditTwoTone, LockOutlined} from "@ant-design/icons";
import styles from "./style.module.css";
import {
    APIInterface,
    handleApolloError,
    useAuthMutation
} from "../../../../services/graphql";
import {UPDATE_PASSWORD_MUTATION} from "../../queries";
import {
    CONFIRM_PASSWORD_VALIDATION_RULES,
    NEW_PASSWORD_VALIDATION_RULES,
    PASSWORD_VALIDATION_RULES
} from "../../../../services/validation";
import {NamePath} from "rc-field-form/lib/interface";

type UpdatePasswordType = APIInterface;

const ProfileItem: React.FC = () => {
    const [form] = Form.useForm();

    const [editing, setEditing] = useState<boolean>(false);
    const [invalidPassword, setInvalidPassword] = useState<boolean>(false);

    const [updatePassword] = useAuthMutation(UPDATE_PASSWORD_MUTATION, {
        onCompleted: async ({updatePassword}: { updatePassword: UpdatePasswordType }) => {
            if (updatePassword.success) {
                setEditing(false);
                await message.success("Successfully edited your password");
            } else {
                const error = updatePassword.errors.nonFieldErrors[0];
                if (error?.code == "invalid_password") {
                    setInvalidPassword(true);
                    await message.error("Incorrect password");
                } else {
                    await message.error(error?.message);
                }
            }
        },
        onError: handleApolloError(() => {
            setEditing(false);
        }),
    });

    type FormValues = {
        oldPassword: string;
        password1: string;
        password2: string;
    }
    const onSubmit = async (values: FormValues) => {
        console.log(values);
        await updatePassword({
            variables: {
                oldPassword: values.oldPassword,
                password: values.password1
            }
        });
    };

    const onChange: (() => void) = () => {
        setInvalidPassword(false);
    };

    if (editing) {
        return <Card hoverable>
            <div className={styles.content}>
                <Card.Meta title="Password"/>
            </div>
            <Form form={form}
                  onFinish={onSubmit}
                  onFieldsChange={onChange}>
                <Form.Item
                    name="oldPassword"
                    initialValue=""
                    rules={PASSWORD_VALIDATION_RULES}
                    validateStatus={invalidPassword ? "error" : ""}
                    hasFeedback
                    className={styles.formItem}
                >
                    <Input.Password prefix={<LockOutlined/>}
                                    placeholder="Password"/>
                </Form.Item>
                <Form.Item
                    name="password1"
                    initialValue=""
                    rules={NEW_PASSWORD_VALIDATION_RULES}
                    hasFeedback
                    className={styles.formItem}
                >
                    <Input.Password prefix={<LockOutlined/>}
                                    placeholder="New password"/>
                </Form.Item>
                <Form.Item
                    name="password2"
                    initialValue=""
                    dependencies={["password1" as NamePath]}
                    rules={CONFIRM_PASSWORD_VALIDATION_RULES}
                    hasFeedback
                    className={styles.formItem}
                >
                    <Input.Password
                        prefix={<LockOutlined/>}
                        placeholder="Confirm new password"
                    />
                </Form.Item>
                <Form.Item shouldUpdate noStyle>
                    {() =>
                        <Button type="primary"
                                htmlType="submit"
                                disabled={
                                    !form.isFieldsTouched(["oldPassword", "password1", "password2"], true) ||
                                    !!form.getFieldsError().filter(({errors}) => errors.length).length
                                }
                        >
                            Change password
                        </Button>
                    }
                </Form.Item>
            </Form>
        </Card>;
    } else {
        return <Card hoverable onClick={() => setEditing(true)}>
            <div className={styles.content}>
                <Card.Meta title="Password"
                           description="**********"/>
                <EditTwoTone className={styles.editButton}/>
            </div>
        </Card>;
    }
};

export default ProfileItem;