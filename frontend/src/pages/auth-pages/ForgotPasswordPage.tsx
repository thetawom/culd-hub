import React from "react";
import AuthBox from "./AuthBox";
import {Alert, Button, Form, Input, message} from "antd";
import {EMAIL_VALIDATION_RULES} from "../../utils/user-field-validation";
import {toLowerCase} from "../../utils/text-utils";
import {MailOutlined} from "@ant-design/icons";
import {Link, useNavigate} from "react-router-dom";

const ForgotPasswordPage: React.FC = () => {

    const [form] = Form.useForm();

    const navigate = useNavigate();

    type FormValues = {
        email: string;
        password: string;
        firstName: string;
        lastName: string;
        phone: string;
    }
    const onFinish = (values: FormValues) => {
        message.success("Reset password email sent.");
        navigate("/login");
    };

    const subtitle = (
        <>
            Remembered your password?{" "}
            <Link to="/login">
                <span style={{fontWeight: "bold"}}>Log in!</span>
            </Link>
        </>
    );

    const alert = <Alert
        type="info"
        message="Enter your registered email below for instructions on resetting your password."
        banner
    />;

    return (
        <AuthBox subtitle={subtitle} alert={alert}>
            <Form
                form={form}
                name="password_reset"
                onFinish={onFinish}
            >
                <Form.Item
                    name="email"
                    rules={EMAIL_VALIDATION_RULES}
                    normalize={toLowerCase}
                >
                    <Input prefix={<MailOutlined/>}
                           placeholder="Email address"/>
                </Form.Item>
                <Form.Item shouldUpdate>
                    {() => (
                        <Button
                            type="primary"
                            htmlType="submit"
                            disabled={
                                !form.isFieldsTouched(["email"], true) ||
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

export default ForgotPasswordPage;