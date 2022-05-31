import React, { useContext } from "react";
import { Link } from "react-router-dom";
import { Form, Input, Button } from "antd";
import { UserOutlined, LockOutlined } from "@ant-design/icons";
import AuthContext from "../context/AuthContext";
import AuthBox from "../components/AuthBox";

const LoginPage = () => {
	let { loginUser } = useContext(AuthContext);
	const [form] = Form.useForm();
	let subtitle = (
		<>
			Don't have an account?{" "}
			<Link to="/signup">
				<span style={{ fontWeight: "bold" }}>Sign up!</span>
			</Link>
		</>
	);
	return (
		<AuthBox subtitle={subtitle}>
			<Form form={form} name="login" onFinish={loginUser}>
				<Form.Item
					name="email"
					rules={[
						{ required: true, message: "Please enter your email address!" },
					]}
				>
					<Input prefix={<UserOutlined />} placeholder="Email address" />
				</Form.Item>
				<Form.Item
					name="password"
					rules={[{ required: true, message: "Please enter your password!" }]}
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
