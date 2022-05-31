import "./App.css";
import { Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import SignupPage from "./pages/SignupPage";
import PrivateRoute from "./utils/PrivateRoute";
import { AuthProvider } from "./context/AuthContext";

function App() {
	return (
		<div className="App">
			<AuthProvider>
				<Routes>
					<Route
						exact
						path="/"
						element={
							<PrivateRoute>
								<HomePage />
							</PrivateRoute>
						}
					/>
					<Route path="login/" element={<LoginPage />} />
					<Route path="signup/" element={<SignupPage />} />
				</Routes>
			</AuthProvider>
		</div>
	);
}

export default App;
