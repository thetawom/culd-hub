import React, { useContext } from "react";
import { Link } from "react-router-dom";
import { Alert, Form, Input, Button } from "antd";
import { MailOutlined, LockOutlined } from "@ant-design/icons";
import AuthContext from "../context/AuthContext";
import AuthBox from "../components/AuthBox";

const LoginPage = () => {
	let { loginUser, invalidCredentials, setInvalidCredentials } =
		useContext(AuthContext);

	let [form] = Form.useForm();

	let onChange = () => {
		setInvalidCredentials(false);
	};

	let subtitle = (
		<>
			Don't have an account?{" "}
			<Link to="/signup">
				<span style={{ fontWeight: "bold" }}>Sign up!</span>
			</Link>
		</>
	);

	let alert = invalidCredentials ? (
		<Alert type="error" message="Username or password are incorrect." banner />
	) : null;

	return (
		<AuthBox subtitle={subtitle} alert={alert}>
			<Form form={form} name="login" onFinish={loginUser}>
				<Form.Item
					name="email"
					rules={[
						{ required: true, message: "Please enter your email address." },
					]}
					validateStatus={invalidCredentials ? "error" : ""}
					hasFeedback={invalidCredentials}
					onChange={onChange}
				>
					<Input prefix={<MailOutlined />} placeholder="Email address" />
				</Form.Item>
				<Form.Item
					name="password"
					rules={[{ required: true, message: "Please enter your password." }]}
					validateStatus={invalidCredentials ? "error" : ""}
					hasFeedback={invalidCredentials}
					onChange={onChange}
				>
					<Input.Password prefix={<LockOutlined />} placeholder="Password" />
				</Form.Item>
				<Form.Item shouldUpdate>
					{() => (
						<Button
							type="primary"
							htmlType="submit"
							disabled={
								!form.isFieldsTouched(false) ||
								!!form.getFieldsError().filter(({ errors }) => errors.length)
									.length
							}
							style={{ width: "100%" }}
						>
							Log in
						</Button>
					)}
				</Form.Item>
			</Form>
		</AuthBox>
	);
};

export default LoginPage;
