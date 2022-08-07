import React, {useState} from "react";
import {Link, useNavigate} from "react-router-dom";
import {Alert, Button, Form, Input, message} from "antd";
import {LockOutlined, MailOutlined, PhoneOutlined, UserOutlined,} from "@ant-design/icons";
import AuthBox from "../components/AuthBox";
import {gql, useMutation} from "@apollo/client";
import {REMEMBER_EMAIL} from "../constants";
import {emailValidationRules, firstNameValidationRules, lastNameValidationRules, phoneValidationRules} from "../utils/user-field-validation";
import {toLowerCase, toTitleCase} from "../utils/text-utils";

export const CREATE_USER_MUTATION = gql`
	mutation CreateUser(
		$email: String!
		$password: String!
		$firstName: String!
		$lastName: String!
		$phone: String!
	) {
		createUser(
			email: $email
			password: $password
			firstName: $firstName
			lastName: $lastName
			phone: $phone
		) {
			user {
				id
				firstName
				lastName
				email
				phone
			}
		}
	}
`;

const SignupPage = () => {
    const [form] = Form.useForm();

    const navigate = useNavigate();

    let [invalidEmail, setInvalidEmail] = useState(false);

    let onChange = () => {
        setInvalidEmail(false);
    };

    let [createUser] = useMutation(CREATE_USER_MUTATION, {
        onCompleted: ({createUser}) => {
            setInvalidEmail(false);
            localStorage.setItem(REMEMBER_EMAIL, createUser.user.email);
            message.success("Account created successfully.");
            navigate("/login");
        },
        onError: (error) => {
            console.log(error.message);
            if (error.message.startsWith("UNIQUE constraint failed")) {
                setInvalidEmail(true);
            }
        },
    });

    const onFinish = (values) => {
        createUser({
            variables: {
                email: values.email,
                password: values.password,
                firstName: values.firstName,
                lastName: values.lastName,
                phone: values.phone ? values.phone : "",
            },
        });
    };

    let subtitle = (
        <>
            Already have an account?{" "}
            <Link to="/login">
                <span style={{fontWeight: "bold"}}>Log in!</span>
            </Link>
        </>
    );

    let alert = invalidEmail ? (
        <Alert
            type="error"
            message="Account with the same email already exists."
            banner
        />
    ) : null;

    return (
        <AuthBox subtitle={subtitle} alert={alert}>
            <Form form={form} name="register" onFinish={onFinish}>
                <Form.Item>
                    <Input.Group compact>
                        <Form.Item
                            name="firstName"
                            rules={firstNameValidationRules}
                            normalize={toTitleCase}
                            noStyle
                        >
                            <Input
                                prefix={<UserOutlined/>}
                                placeholder="First name"
                                style={{width: "50%"}}
                            />
                        </Form.Item>
                        <Form.Item
                            name="lastName"
                            rules={lastNameValidationRules}
                            normalize={toTitleCase}
                            noStyle
                        >
                            <Input placeholder="Last name" style={{width: "50%"}}/>
                        </Form.Item>
                    </Input.Group>
                </Form.Item>
                <Form.Item
                    name="email"
                    rules={emailValidationRules}
                    validateStatus={invalidEmail ? "error" : ""}
                    hasFeedback={invalidEmail}
                    onChange={onChange}
                    normalize={toLowerCase}
                >
                    <Input prefix={<MailOutlined/>} placeholder="Email address"/>
                </Form.Item>
                <Form.Item
                    name="phone"
                    rules={phoneValidationRules}
                >
                    <Input placeholder="Phone number" prefix={<PhoneOutlined/>}/>
                </Form.Item>
                <Form.Item
                    name="password"
                    rules={[{required: true, message: "Please enter your password."}]}
                    hasFeedback
                >
                    <Input.Password prefix={<LockOutlined/>} placeholder="Password"/>
                </Form.Item>
                <Form.Item
                    name="confirm"
                    depndencies={["password"]}
                    rules={[
                        {required: true, message: "Please confirm your password."},
                        ({getFieldValue}) => ({
                            validator(_, value) {
                                if (!value || getFieldValue("password") === value) {
                                    return Promise.resolve();
                                }

                                return Promise.reject(
                                    new Error("The two passwords that you entered do not match.")
                                );
                            },
                        }),
                    ]}
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
                                !form.isFieldsTouched(
                                    ["firstName", "lastName", "email", "password", "confirm"],
                                    true
                                ) ||
                                !!form.getFieldsError().filter(({errors}) => errors.length)
                                    .length
                            }
                            style={{width: "100%"}}
                        >
                            Register
                        </Button>
                    )}
                </Form.Item>
            </Form>
        </AuthBox>
    );
};

export default SignupPage;
