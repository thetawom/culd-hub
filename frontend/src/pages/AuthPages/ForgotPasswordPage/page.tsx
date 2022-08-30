import React, {useEffect, useState} from "react";
import AuthPage from "../template";
import {Alert, Button, Form, Input, message} from "antd";
import {EMAIL_VALIDATION_RULES, toLowerCase} from "../../../services/validation";
import {MailOutlined} from "@ant-design/icons";
import {Link} from "react-router-dom";
import {useMutation} from "@apollo/client";
import {SEND_PASSWORD_RESET_EMAIL_MUTATION} from "./queries";
import {APIInterface, handleApolloError} from "../../../services/graphql";
import {RESEND_PASSWORD_RESET_EMAIL_TIMEOUT_SECONDS} from "./constants";


export const ForgotPasswordPage: React.FC = () => {

    const [form] = Form.useForm();
    const [email, setEmail] = useState(null);
    const [submitted, setSubmitted] = useState(false);
    const [loading, setLoading] = useState(false);
    const [resendTimeoutSeconds, setResendTimeoutSeconds] = useState(0);

    const [sendPasswordResetEmail] = useMutation(SEND_PASSWORD_RESET_EMAIL_MUTATION, {
            onCompleted: async ({sendPasswordResetEmail}: { sendPasswordResetEmail: APIInterface }) => {
                setLoading(false);
                if (sendPasswordResetEmail.success) {
                    setSubmitted(true);
                    setResendTimeoutSeconds(RESEND_PASSWORD_RESET_EMAIL_TIMEOUT_SECONDS);
                } else {
                    console.log(sendPasswordResetEmail.errors);
                    await message.error("Sorry, there was an error sending your password reset email");
                    setEmail(null);
                    setSubmitted(false);
                }
            },
            onError: handleApolloError(() => {
                setLoading(false);
            })
        }
    );

    useEffect(() => {
        if (resendTimeoutSeconds > 0) {
            setTimeout(() => setResendTimeoutSeconds(resendTimeoutSeconds - 1), 1000);
        }
    }, [resendTimeoutSeconds]);

    type FormValues = {
        email: string; password: string; firstName: string; lastName: string; phone: string;
    }
    const onFinish = async (values: FormValues) => {
        setEmail(() => values.email);
        await submitEmail(values.email);
    };

    const submitEmail = async (email: string) => {
        setLoading(true);
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

    return (<AuthPage subtitle={subtitle}>
        {submitted ?
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
                        disabled={loading || resendTimeoutSeconds > 0}
                        loading={loading}
                    >
                        {resendTimeoutSeconds > 0 ? `Resend reset link in ${resendTimeoutSeconds} seconds` : "Resend reset link"}
                    </Button>
                </Form.Item>
            </> :
            <>
                <Alert
                    type="info"
                    message="Enter your registered email address below for a one-time link to reset your password."
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
                        validateTrigger="onBlur"
                        normalize={toLowerCase}
                    >
                        <Input prefix={<MailOutlined/>}
                               placeholder="Email address"/>
                    </Form.Item>
                    <Form.Item shouldUpdate>
                        {() => (<Button
                            type="primary"
                            htmlType="submit"
                            disabled={
                                loading
                                || !form.isFieldsTouched(["email"], true)
                                || !!form.getFieldsError().filter(({errors}) => errors.length).length
                            }
                            style={{width: "100%"}}
                            loading={loading}
                        >
                            Reset my password
                        </Button>)}
                    </Form.Item>
                </Form>
            </>
        }
    </AuthPage>);
};