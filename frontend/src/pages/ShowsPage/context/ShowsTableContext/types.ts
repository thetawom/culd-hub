import {Show} from "../../../../types/types";

export interface ShowContextInterface {
    shows: Show[],
    showPriorityChoices: object,
    openFilter: string,
    needsRefresh: boolean,
    setOpenFilter: (openFilter: string) => void,
    setNeedsRefresh: (needsRefresh: boolean) => void,
    addToShowRoster: (id: number) => void,
    removeFromShowRoster: (id: number) => void,
}