import {Show} from "../../../../types/types";
import {Options, Views} from "../../components/ShowsTableControls";

export interface ShowContextInterface {
    shows: Show[],
    showPriorityChoices: object,
    showStatusChoices: object,
    view: Views,
    optionsFilter: Options,
    needsRefresh: boolean,
    setView: (view: Views) => void,
    setOptionsFilter: (optionsFilter: Options) => void,
    setNeedsRefresh: (needsRefresh: boolean) => void,
    addToShowRoster: (id: number) => void,
    removeFromShowRoster: (id: number) => void,
}