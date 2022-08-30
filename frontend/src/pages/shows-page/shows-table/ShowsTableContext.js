import React, {createContext, useContext, useEffect, useState} from "react";
import {message} from "antd";
import PropTypes from "prop-types";
import {handleApolloError, useAuthLazyQuery, useAuthMutation, useAuthQuery} from "../../../services/graphql";
import {AuthContext} from "../../../context/AuthContext";
import {gql} from "@apollo/client";

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
    useAuthQuery(GET_SHOW_PRIORITY_CHOICES_QUERY, {
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
        const fetchShows = async () => {
            await getShows();
        };
        fetchShows().catch(console.error);
    }, [needsRefresh, getShows]);

    let [createRole] = useAuthMutation(CREATE_ROLE_MUTATION, {
        onCompleted: async ({createRole}) => {
            setShows(shows.map((show) => show.id === createRole.role.show.id ? {
                ...show,
                performers: [...show.performers, createRole.role.performer],
            } : {...show}));
            await message.success(`Signed up for ${createRole.role.show.name}`);
        },
        onError: handleApolloError,
    });

    let addToShowRoster = async (id) => {
        if (shows.find((show) => show.id === id).isOpen) {
            await createRole({
                variables: {
                    showId: id,
                },
            });
        }
    };

    let [deleteRole] = useAuthMutation(DELETE_ROLE_MUTATION, {
        onCompleted: async ({deleteRole}) => {
            setShows(shows.map((show) => show.id === deleteRole.role.show.id ? {
                ...show,
                performers: show.performers.filter((performer) => performer.user.id !== deleteRole.role.performer.user.id),
            } : {...show}));
            await message.success(`Removed from ${deleteRole.role.show.name}`);
        },
        onError: handleApolloError,
    });

    let removeFromShowRoster = async (id) => {
        if (shows.find((show) => show.id === id).isOpen) {
            await deleteRole({
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

ShowsTableProvider.propTypes = {
    children: PropTypes.arrayOf(PropTypes.element),
};