import React, { useContext } from "react";
import { Link } from "react-router-dom";
import { Form } from "antd";
import AuthContext from "../context/AuthContext";
import AuthBox from "../components/AuthBox";

const SignupPage = () => {
	let { loginUser } = useContext(AuthContext);
	const [form] = Form.useForm();
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
			<Form form={form} name="login" onFinish={loginUser}></Form>
		</AuthBox>
	);
};

export default SignupPage;
