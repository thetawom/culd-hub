import React, {createContext, useContext, useEffect, useState} from "react";
import {message} from "antd";
import PropTypes from "prop-types";
import {handleApolloError, useAuthLazyQuery, useAuthMutation, useAuthQuery} from "../../../../services/graphql";
import {AuthContext} from "../../../../context/AuthContext";
import {CREATE_ROLE_MUTATION, DELETE_ROLE_MUTATION, GET_SHOW_PRIORITY_CHOICES_QUERY, GET_SHOWS_QUERY} from "./queries";

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