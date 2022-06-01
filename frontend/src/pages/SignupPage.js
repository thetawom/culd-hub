import React from "react";
import { Link } from "react-router-dom";
import { Form, Input, Button } from "antd";
import {
	UserOutlined,
	MailOutlined,
	PhoneOutlined,
	LockOutlined,
} from "@ant-design/icons";
import AuthBox from "../components/AuthBox";

const SignupPage = () => {
	const [form] = Form.useForm();

	const onFinish = (values) => {
		console.log(values);
	};

	const toLowerCase = (str) => (str || "").toLowerCase();

	const toTitleCase = (str) =>
		str &&
		(str[0].toUpperCase() + str.substr(1).toLowerCase()).replace(" ", "");

	let subtitle = (
		<>
			Already have an account?{" "}
			<Link to="/login">
				<span style={{ fontWeight: "bold" }}>Log in!</span>
			</Link>
		</>
	);

	return (
		<AuthBox subtitle={subtitle}>
			<Form form={form} name="register" onFinish={onFinish}>
				<Form.Item>
					<Input.Group compact>
						<Form.Item
							name="first_name"
							rules={[
								{ required: true, message: "Please enter your first name." },
							]}
							normalize={toTitleCase}
							noStyle
						>
							<Input
								prefix={<UserOutlined />}
								placeholder="First name"
								style={{ width: "50%" }}
							/>
						</Form.Item>
						<Form.Item
							name="last_name"
							rules={[
								{ required: true, message: "Please enter your last name." },
							]}
							normalize={toTitleCase}
							noStyle
						>
							<Input placeholder="Last name" style={{ width: "50%" }} />
						</Form.Item>
					</Input.Group>
				</Form.Item>
				<Form.Item
					name="email"
					rules={[
						{ type: "email", message: "This is not a valid email address." },
						{ required: true, message: "Please enter your email address." },
					]}
					normalize={toLowerCase}
				>
					<Input prefix={<MailOutlined />} placeholder="Email address" />
				</Form.Item>
				<Form.Item
					name="phone_number"
					rules={[
						{
							pattern: new RegExp(
								/(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$/g
							),
							message: "This is not a valid phone number.",
						},
					]}
				>
					<Input placeholder="Phone number" prefix={<PhoneOutlined />} />
				</Form.Item>
				<Form.Item
					name="password"
					rules={[{ required: true, message: "Please enter your password." }]}
					hasFeedback
				>
					<Input.Password prefix={<LockOutlined />} placeholder="Password" />
				</Form.Item>
				<Form.Item
					name="confirm"
					depndencies={["password"]}
					rules={[
						{ required: true, message: "Please confirm your password." },
						({ getFieldValue }) => ({
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
						prefix={<LockOutlined />}
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
									["first_name", "last_name", "email", "password", "confirm"],
									true
								) ||
								!!form.getFieldsError().filter(({ errors }) => errors.length)
									.length
							}
							style={{ width: "100%" }}
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
