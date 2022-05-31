import "./App.css";
import { gql, useQuery } from "@apollo/client";

const GET_USERS = gql`
	{
		users {
			id
			firstName
			lastName
		}
	}
`;

function App() {
	const { loading, error, data } = useQuery(GET_USERS);
	if (loading) return "Loading ...";
	if (error) return `Error! ${error.message}`;
	console.log(data);
	return (
		<div className="App">
			{data.users.map(({ id, firstName, lastName }) => (
				<p key={id}>
					{firstName} {lastName}
				</p>
			))}
		</div>
	);
}

export default App;
