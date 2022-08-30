import React, {useState} from "react";
import {Link, useNavigate, useParams} from "react-router-dom";
import {Alert, Button, Form, Input, message} from "antd";
import {LockOutlined} from "@ant-design/icons";
import {NamePath} from "rc-field-form/lib/interface";
import {CONFIRM_PASSWORD_VALIDATION_RULES, PASSWORD_VALIDATION_RULES} from "../../../services/validation";
import {APIInterface, handleApolloError, useMutation} from "../../../services/graphql";
import AuthPage from "../template";
import {RESET_PASSWORD_MUTATION} from "./queries";

export const ResetPasswordPage: React.FC = () => {
    const params = useParams();

    const [form] = Form.useForm();
    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);

    const [resetPassword] = useMutation(RESET_PASSWORD_MUTATION, {
        onCompleted: async ({resetPassword}: { resetPassword: APIInterface }) => {
            setLoading(false);
            if (resetPassword.success) {
                navigate("/login");
                await message.success("Password reset successfully.");
            } else {
                const error = resetPassword.errors.nonFieldErrors[0];
                switch (error?.code) {
                    case "invalid_token":
                        navigate("/password_reset");
                        await message.error("Sorry, your password reset link has already expired.");
                        break;
                    default:
                        await message.error(error?.message);
                }
            }
        },
        onError: handleApolloError(() => {
            setLoading(false);
        }),
    });

    const [invalidPassword, setInvalidPassword] = useState(false);

    const onChange = () => {
        setInvalidPassword(false);
    };

    type FormValues = {
        password1: string;
        password2: string;
    }
    const onFinish = async (values: FormValues) => {
        setLoading(true);
        await resetPassword({
            variables: {
                userId: params.userId,
                token: params.token,
                password: values.password1
            }
        });
    };

    const subtitle = (<>
        Reset your password below. Then{" "}
        <Link to="/login">
            <span style={{fontWeight: "bold"}}>log in!</span>
        </Link>
    </>);

    const alert = invalidPassword ? (
        <Alert
            type="error"
            message="New and old passwords must be different."
            banner
        />
    ) : null;

    return (
        <AuthPage subtitle={subtitle} alert={alert}>
            <Form
                form={form}
                name="register"
                onFinish={onFinish}
                onFieldsChange={onChange}
            >
                <Form.Item
                    name="password1"
                    rules={PASSWORD_VALIDATION_RULES}
                    hasFeedback
                >
                    <Input.Password prefix={<LockOutlined/>}
                                    placeholder="Password"/>
                </Form.Item>
                <Form.Item
                    name="password2"
                    dependencies={["password1" as NamePath]}
                    rules={CONFIRM_PASSWORD_VALIDATION_RULES}
                    hasFeedback
                >
                    <Input.Password
                        prefix={<LockOutlined/>}
                        placeholder="Confirm password"
                    />
                </Form.Item>
                <Form.Item shouldUpdate>
                    {() => (
                        <Button
                            type="primary"
                            htmlType="submit"
                            disabled={
                                !form.isFieldsTouched(["password1", "password2"], true)
                                || !!form.getFieldsError().filter(({errors}) => errors.length).length
                            }
                            loading={loading}
                            style={{width: "100%"}}
                        >
                            Reset my password
                        </Button>
                    )}
                </Form.Item>
            </Form>
        </AuthPage>
    );
};