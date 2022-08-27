import React, {useState} from "react";
import AuthBox from "./AuthBox";
import {Link, useNavigate, useParams} from "react-router-dom";
import {Alert, Button, Form, Input, message} from "antd";
import {LockOutlined} from "@ant-design/icons";
import {NamePath} from "rc-field-form/lib/interface";
import {CONFIRM_PASSWORD_VALIDATION_RULES, PASSWORD_VALIDATION_RULES} from "../../utils/user-field-validation";
import {ApolloError, gql, useMutation} from "@apollo/client";

export const RESET_PASSWORD_MUTATION = gql`
    mutation ResetPassword (
        $token: String!
        $password: String!
    ) {
        resetPassword(
            token: $token
            password: $password
        ) {
            success
            errors
        }
    }
`;

const ResetPasswordPage: React.FC = () => {
    const params = useParams();

    const [form] = Form.useForm();

    const navigate = useNavigate();

    const [resetPassword] = useMutation(RESET_PASSWORD_MUTATION, {
        onCompleted: async () => {
            await message.success("Password reset successfully.");
            navigate("/login");
        },
        onError: async (error: ApolloError) => {
            console.log(error.message);
            if (error.networkError) {
                await message.error("Failed to connect to server");
            } else {
                await message.error(error.message);
            }
        },
    });

    const [invalidPassword, setInvalidPassword] = useState(false);

    const onChange = () => {
        setInvalidPassword(false);
    };

    type FormValues = {
        password: string;
        confirm: string;
    }
    const onFinish = async (values: FormValues) => {
        await resetPassword({
            variables: {
                token: params.token,
                password: values.password
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
        <AuthBox subtitle={subtitle} alert={alert}>
            <Form
                form={form}
                name="register"
                onFinish={onFinish}
                onFieldsChange={onChange}
            >
                <Form.Item
                    name="password"
                    rules={PASSWORD_VALIDATION_RULES}
                    hasFeedback
                >
                    <Input.Password prefix={<LockOutlined/>}
                                    placeholder="Password"/>
                </Form.Item>
                <Form.Item
                    name="confirm"
                    dependencies={["password" as NamePath]}
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
                                !form.isFieldsTouched(["password", "confirm"], true) ||
                                !!form.getFieldsError().filter(({errors}) => errors.length).length
                            }
                            style={{width: "100%"}}
                        >
                            Reset my password
                        </Button>
                    )}
                </Form.Item>
            </Form>
        </AuthBox>
    );
};

export default ResetPasswordPage;