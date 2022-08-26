import React, {useEffect, useState} from "react";
import AuthBox from "./AuthBox";
import {Alert, Button, Form, Input} from "antd";
import {EMAIL_VALIDATION_RULES} from "../../utils/user-field-validation";
import {toLowerCase} from "../../utils/text-utils";
import {MailOutlined} from "@ant-design/icons";
import {Link} from "react-router-dom";
import {gql, useMutation} from "@apollo/client";

export const SEND_PASSWORD_RESET_EMAIL_MUTATION = gql`
    mutation SendPasswordResetEmail ($email: String!) {
        sendPasswordResetEmail(email: $email) {
            success
            errors
        }
    }
`;

const ForgotPasswordPage: React.FC = () => {

    const [form] = Form.useForm();

    const [email, setEmail] = useState(null);

    const [sendPasswordResetEmail] = useMutation(SEND_PASSWORD_RESET_EMAIL_MUTATION);

    const [resendTimeout, setResendTimeout] = useState(0);

    useEffect(() => {
        if (resendTimeout > 0) {
            setTimeout(() => setResendTimeout(resendTimeout - 1), 1000);
        }
    }, [resendTimeout]);

    type FormValues = {
        email: string; password: string; firstName: string; lastName: string; phone: string;
    }
    const onFinish = async (values: FormValues) => {
        setEmail(() => values.email);
        await submitEmail(values.email);
    };

    const submitEmail = async (email: string) => {
        setResendTimeout(59);
        await sendPasswordResetEmail({
            variables: {
                email: email,
            },
        });
    };

    const subtitle = (<>
        Remembered your password?{" "}
        <Link to="/login">
            <span style={{fontWeight: "bold"}}>Log in!</span>
        </Link>
    </>);

    return (<AuthBox subtitle={subtitle}>
        {email ?
            <>
                <Alert
                    type="success"
                    message="If the email you entered is correct, you will receive your password reset link shortly."
                    banner
                    style={{marginBottom: "1.5em"}}
                />
                <Form.Item shouldUpdate>
                    <Button
                        onClick={() => submitEmail(email)}
                        style={{width: "100%"}}
                        disabled={resendTimeout > 0}
                    >
                        {resendTimeout > 0 ? `Resend reset link in ${resendTimeout} seconds` : "Resend reset link"}
                    </Button>
                </Form.Item>
            </> :
            <>
                <Alert
                    type="info"
                    message="Enter your registered email address below for a link to reset your password."
                    banner
                    style={{marginBottom: "1.5em"}}
                />
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
                        {() => (<Button
                            type="primary"
                            htmlType="submit"
                            disabled={!form.isFieldsTouched(["email"], true)
                                || !!form.getFieldsError().filter(({errors}) => errors.length).length}
                            style={{width: "100%"}}
                        >
                            Reset my password
                        </Button>)}
                    </Form.Item>
                </Form>
            </>
        }
    </AuthBox>);
};

export default ForgotPasswordPage;