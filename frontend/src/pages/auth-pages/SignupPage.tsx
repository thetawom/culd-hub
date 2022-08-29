import React from "react";
import {Link, useNavigate} from "react-router-dom";
import {Button, Form, Input, message} from "antd";
import {NamePath} from "rc-field-form/lib/interface";
import {LockOutlined, MailOutlined, PhoneOutlined, UserOutlined,} from "@ant-design/icons";
import AuthBox from "./AuthBox";
import {gql, useMutation} from "@apollo/client";
import {REMEMBER_EMAIL} from "../../constants";
import {
    CONFIRM_PASSWORD_VALIDATION_RULES,
    EMAIL_VALIDATION_RULES,
    FIRST_NAME_VALIDATION_RULES,
    LAST_NAME_VALIDATION_RULES,
    PASSWORD_VALIDATION_RULES,
    PHONE_VALIDATION_RULES
} from "../../utils/validate.utils";
import {toLowerCase, toTitleCase} from "../../utils/normalize.utils";
import {APIInterface, UserType} from "../../interfaces/api.interface";
import styles from "./SignupPage.module.css";
import {onApolloError} from "../../utils/graphql.utils";

export const REGISTER_MUTATION = gql`
	mutation Register(
		$email: String!
		$password1: String!
		$password2: String!
		$firstName: String!
		$lastName: String!
		$phone: String!
	) {
		register(
			email: $email
			password1: $password1
			password2: $password2
			firstName: $firstName
			lastName: $lastName
			phone: $phone
		) {
		    success
		    errors
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

type RegisterType = APIInterface & {
    user: UserType;
}

const SignupPage = () => {
    const [form] = Form.useForm();

    const navigate = useNavigate();

    const [createUser] = useMutation(REGISTER_MUTATION, {
        onCompleted: async ({register}: { register: RegisterType }) => {
            if (register.success) {
                localStorage.setItem(REMEMBER_EMAIL, register.user.email);
                navigate("/login");
                await message.success("Account created successfully.");
            } else {
                const errors = Object.entries(register.errors).map(
                    ([field, errors]) => ({
                        name: field,
                        errors: errors.map(error => error.message)
                    }));
                form.setFields(errors);
            }
        },
        onError: onApolloError,
    });

    type FormValues = {
        email: string;
        password1: string;
        password2: string;
        firstName: string;
        lastName: string;
        phone: string;
    }
    const onFinish = async (values: FormValues) => {
        await createUser({
            variables: {
                email: values.email,
                password1: values.password1,
                password2: values.password2,
                firstName: values.firstName,
                lastName: values.lastName,
                phone: values.phone ? values.phone : "",
            },
        });
    };

    const subtitle = (
        <div className={styles.subtitle}>
            Already have an account?{" "}
            <Link to="/login">Log in!</Link>
        </div>
    );

    return (
        <AuthBox subtitle={subtitle}>
            <Form
                form={form}
                name="register"
                onFinish={onFinish}
            >
                <Form.Item>
                    <Input.Group compact>
                        <Form.Item
                            name="firstName"
                            rules={FIRST_NAME_VALIDATION_RULES}
                            validateTrigger="onBlur"
                            normalize={toTitleCase}
                            noStyle
                        >
                            <Input
                                prefix={<UserOutlined/>}
                                placeholder="First name"
                                className={styles.halfInput}
                            />
                        </Form.Item>
                        <Form.Item
                            name="lastName"
                            rules={LAST_NAME_VALIDATION_RULES}
                            validateTrigger="onBlur"
                            normalize={toTitleCase}
                            noStyle
                        >
                            <Input
                                placeholder="Last name"
                                className={styles.halfInput}
                            />
                        </Form.Item>
                    </Input.Group>
                </Form.Item>
                <Form.Item
                    name="email"
                    rules={EMAIL_VALIDATION_RULES}
                    validateTrigger="onBlur"
                    normalize={toLowerCase}
                >
                    <Input prefix={<MailOutlined/>}
                           placeholder="Email address"/>
                </Form.Item>
                <Form.Item
                    name="phone"
                    rules={PHONE_VALIDATION_RULES}
                    validateTrigger="onBlur"
                >
                    <Input placeholder="Phone number"
                           prefix={<PhoneOutlined/>}/>
                </Form.Item>
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
                                !form.isFieldsTouched(["firstName", "lastName", "email", "password1", "password2"], true) ||
                                !!form.getFieldsError().filter(({errors}) => errors.length).length
                            }
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
