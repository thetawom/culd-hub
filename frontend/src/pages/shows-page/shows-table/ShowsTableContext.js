import React, {createContext, useContext, useEffect, useState} from "react";
import {message} from "antd";
import {gql} from "@apollo/client";
import useAuthMutation from "../../../utils/hooks/useAuthMutation";
import AuthContext from "../../../context/AuthContext";
import useAuthLazyQuery from "../../../utils/hooks/useAuthLazyQuery";
import useAuthQuery from "../../../utils/hooks/useAuthQuery";

const GET_SHOWS_QUERY = gql`
	{
		shows {
			id
			name
			priority
			date
			time
			rounds {
				id
				time
			}
			address
			lions
			performers {
				user {
					id
					firstName
					lastName
				}
			}
			point {
				user {
					id
					firstName
					lastName
				}
			}
			contact {
				firstName
				lastName
				phone
				email
			}
			isCampus
			isOpen
		}
	}
`;

export const CREATE_ROLE_MUTATION = gql`
	mutation CreateRole($showId: ID!) {
		createRole(showId: $showId) {
			role {
				show {
					id
					name
				}
				performer {
					user {
						id
						firstName
						lastName
					}
				}
			}
		}
	}
`;

export const DELETE_ROLE_MUTATION = gql`
	mutation DeleteRole($showId: ID!) {
		deleteRole(showId: $showId) {
			role {
				show {
					id
					name
				}
				performer {
					user {
						id
					}
				}
			}
		}
	}
`;

const GET_SHOW_PRIORITY_CHOICES_QUERY = gql`
	{
		showPriorityChoices
	}
`;

const ShowsTableContext = createContext();

export default ShowsTableContext;

export const ShowsTableProvider = ({children}) => {
    let {logoutUser} = useContext(AuthContext);

    let [shows, setShows] = useState([]);

    let [showPriorityChoices, setShowPriorityChoices] = useState(null);
    let {showPriorityChoicesLoading} = useAuthQuery(GET_SHOW_PRIORITY_CHOICES_QUERY, {
        onCompleted: ({showPriorityChoices}) => {
            setShowPriorityChoices(JSON.parse(showPriorityChoices));
        },
    });

    let [openFilter, setOpenFilter] = useState("Open");
    let [needsRefresh, setNeedsRefresh] = useState(true);

    let [getShows] = useAuthLazyQuery(GET_SHOWS_QUERY, {
        onCompleted: ({shows}) => {
            setShows(shows);
            setNeedsRefresh(false);
        },
        onError: () => logoutUser(),
        fetchPolicy: "network-only",
        nextFetchPolicy: "network-only",
    });

    useEffect(() => {
        getShows();
    }, [needsRefresh, getShows]);

    let [createRole] = useAuthMutation(CREATE_ROLE_MUTATION, {
        onCompleted: ({createRole}) => {
            setShows(shows.map((show) => show.id === createRole.role.show.id ? {
                ...show,
                performers: [...show.performers, createRole.role.performer],
            } : {...show}));
            message.success(`Signed up for ${createRole.role.show.name}`);
        }, onError: (error) => {
            console.log(error.message);
        },
    });

    let addToShowRoster = (id) => {
        if (shows.find((show) => show.id === id).isOpen) {
            createRole({
                variables: {
                    showId: id,
                },
            });
        }
    };

    let [deleteRole] = useAuthMutation(DELETE_ROLE_MUTATION, {
        onCompleted: ({deleteRole}) => {
            setShows(shows.map((show) => show.id === deleteRole.role.show.id ? {
                ...show,
                performers: show.performers.filter((performer) => performer.user.id !== deleteRole.role.performer.user.id),
            } : {...show}));
            message.success(`Removed from ${deleteRole.role.show.name}`);
        }, onError: (error) => {
            console.log(error.message);
        },
    });

    let removeFromShowRoster = (id) => {
        if (shows.find((show) => show.id === id).isOpen) {
            deleteRole({
                variables: {
                    showId: id,
                },
            });
        }
    };

    let contextData = {
        shows: shows,
        showPriorityChoices: showPriorityChoices,
        openFilter: openFilter,
        needsRefresh: needsRefresh,
        setOpenFilter: setOpenFilter,
        setNeedsRefresh: setNeedsRefresh,
        addToShowRoster: addToShowRoster,
        removeFromShowRoster: removeFromShowRoster,
    };

    return (<ShowsTableContext.Provider value={contextData}>
        {children}
    </ShowsTableContext.Provider>);
};
