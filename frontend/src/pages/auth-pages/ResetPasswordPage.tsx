import React, {useState} from "react";
import AuthBox from "./AuthBox";
import {Link, useNavigate, useParams} from "react-router-dom";
import {Alert, Button, Form, Input, message} from "antd";
import {LockOutlined} from "@ant-design/icons";
import {NamePath} from "rc-field-form/lib/interface";
import {CONFIRM_PASSWORD_VALIDATION_RULES, PASSWORD_VALIDATION_RULES} from "../../utils/user-field-validation";
import {REMEMBER_EMAIL} from "../../constants";

const ResetPasswordPage: React.FC = () => {
    const params = useParams();

    const [form] = Form.useForm();

    const navigate = useNavigate();

    const [invalidPassword, setInvalidPassword] = useState(false);

    const onChange = () => {
        setInvalidPassword(false);
    };

    type FormValues = {
        password: string;
        confirm: string;
    }
    const onFinish = async (values: FormValues) => {
        console.log(params);
        console.log(values.password);
        setInvalidPassword(true);

        const email = "ew2664@columbia.edu";
        localStorage.setItem(REMEMBER_EMAIL, email);
        navigate("/login");
        await message.success("Password reset successfully.");
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