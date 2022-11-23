import React, {createContext, useContext, useEffect, useState} from "react";
import {message} from "antd";
import {
    handleApolloError,
    useAuthLazyQuery,
    useAuthMutation,
    useAuthQuery
} from "../../../../services/graphql";
import {AuthContext} from "../../../../context/AuthContext";
import {
    CREATE_ROLE_MUTATION,
    DELETE_ROLE_MUTATION,
    GET_SHOW_PRIORITY_CHOICES_QUERY,
    GET_SHOW_STATUS_CHOICES_QUERY,
    GET_SHOWS_QUERY
} from "./queries";
import {Show, User} from "../../../../types/types";
import {ShowContextInterface} from "./types";
import {Options, Views} from "../../components/ShowsTableControls";
import {UserContext} from "../../../../context/UserContext";
import dayjs from "dayjs";

const ShowsTableContext = createContext(undefined);

export default ShowsTableContext;

interface Props {
    children: React.ReactNode[]
}

export const ShowsTableProvider: React.FC<Props> = ({children}: Props) => {
    const {logoutUser} = useContext(AuthContext);
    const {user}: { user: User } = useContext(UserContext);

    const [showPriorityChoices, setShowPriorityChoices] = useState(null);
    useAuthQuery(GET_SHOW_PRIORITY_CHOICES_QUERY, {
        onCompleted: ({showPriorityChoices}) => {
            setShowPriorityChoices(JSON.parse(showPriorityChoices));
        },
    });

    const [showStatusChoices, setShowStatusChoices] = useState(null);
    useAuthQuery(GET_SHOW_STATUS_CHOICES_QUERY, {
        onCompleted: ({showStatusChoices}) => {
            setShowStatusChoices(JSON.parse(showStatusChoices));
        },
    });

    const [view, setView] = useState<Views>(Views.TABLE);
    const [optionsFilter, setOptionsFilter] = useState<Options>(Options.UPCOMING);
    const [needsRefresh, setNeedsRefresh] = useState<boolean>(true);

    const [shows, setShows] = useState<Show[]>([]);
    const [getShows] = useAuthLazyQuery(GET_SHOWS_QUERY, {
        onCompleted: ({shows}) => {
            shows.forEach(show => show.date = dayjs(show.date));
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

    const [createRole] = useAuthMutation(CREATE_ROLE_MUTATION, {
        onCompleted: async ({createRole}) => {
            setShows(shows.map((show) => show.id === createRole.role.show.id ? {
                ...show,
                performers: [...show.performers, createRole.role.performer],
            } : {...show}));
            await message.success(`Signed up for ${createRole.role.show.name}`);
        },
        onError: handleApolloError(),
    });

    const addToShowRoster = async (id: number) => {
        if (shows.find((show: Show) => show.id === id).isOpen) {
            await createRole({
                variables: {
                    showId: id,
                },
            });
        }
    };

    const [deleteRole] = useAuthMutation(DELETE_ROLE_MUTATION, {
        onCompleted: async ({deleteRole}) => {
            setShows(shows.map((show: Show) => show.id === deleteRole.role.show.id ? {
                ...show,
                performers: show.performers.filter((performer) => performer.user.id !== deleteRole.role.performer.user.id),
            } : {...show}));
            await message.success(`Removed from ${deleteRole.role.show.name}`);
        },
        onError: handleApolloError(),
    });

    const removeFromShowRoster = async (id: number) => {
        if (shows.find((show: Show) => show.id === id).isOpen) {
            await deleteRole({
                variables: {
                    showId: id,
                },
            });
        }
    };

    const isPerforming = (show: Show) => {
        for (const performer of show.performers) {
            if (performer.user.id === user.id) return true;
        }
        return false;
    };

    let filtered_shows: Show[];
    switch (optionsFilter) {
        case Options.ALL:
            filtered_shows = shows;
            break;
        case Options.MINE:
            filtered_shows = shows.filter(isPerforming);
            break;
        case Options.UPCOMING:
            filtered_shows = shows.filter((show: Show) => !dayjs().isAfter(show.date, "day"));
            break;
        case Options.PAST:
            filtered_shows = shows.filter((show: Show) => dayjs().isAfter(show.date, "day"));
            break;
    }

    const contextData: ShowContextInterface = {
        shows: filtered_shows,
        showPriorityChoices: showPriorityChoices,
        showStatusChoices: showStatusChoices,
        view: view,
        optionsFilter: optionsFilter,
        needsRefresh: needsRefresh,
        setView: setView,
        setOptionsFilter: setOptionsFilter,
        setNeedsRefresh: setNeedsRefresh,
        addToShowRoster: addToShowRoster,
        removeFromShowRoster: removeFromShowRoster,
    };

    return (
        <ShowsTableContext.Provider value={contextData}>
            {children}
        </ShowsTableContext.Provider>
    );
};