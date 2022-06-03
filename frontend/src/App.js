import "./App.css";
import { Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import ProfilePage from "./pages/ProfilePage";
import LoginPage from "./pages/LoginPage";
import SignupPage from "./pages/SignupPage";
import PrivateRoutes from "./utils/PrivateRoutes";
import { AuthProvider } from "./context/AuthContext";
import { message } from "antd";

function App() {
	message.config({
		duration: 1.5,
	});

	return (
		<div className="App">
			<AuthProvider>
				<Routes>
					<Route element={<PrivateRoutes />}>
						<Route path="/" exact element={<HomePage />} />
						<Route path="profile/" element={<ProfilePage />} />
					</Route>
					<Route path="login/" element={<LoginPage />} />
					<Route path="signup/" element={<SignupPage />} />
				</Routes>
			</AuthProvider>
		</div>
	);
}

export default App;
