import React, {useContext} from "react";
import {
    Button,
    message,
    Modal,
    Progress,
    Space,
    Table,
    Tag,
    Tooltip
} from "antd";
import {
    InfoCircleOutlined,
    InfoCircleTwoTone,
    MailTwoTone,
    PhoneTwoTone,
    PlusOutlined,
    StarFilled,
    WarningFilled
} from "@ant-design/icons";
import dayjs from "dayjs";
import ShowsTableContext from "../../context/ShowsTableContext";
import {OPTIONS_ENUM} from "../ShowsTableControls";
import {Contact, Member, Round, Show, User} from "../../../../types/types";
import {ShowContextInterface} from "../../context/ShowsTableContext/types";
import ShowDetails from "../ShowDetails";

// eslint-disable-next-line @typescript-eslint/no-var-requires
const customParseFormat = require("dayjs/plugin/customParseFormat");
dayjs.extend(customParseFormat);

const ShowsTable = ({user}: { user: User }) => {

    const {
        shows,
        showPriorityChoices,
        openFilter,
        needsRefresh,
        addToShowRoster,
        removeFromShowRoster,
    }: ShowContextInterface = useContext(ShowsTableContext);

    const performersNeeded = (show: Show) => show.lions * 2 + 2;

    const columns = [{
        title: "",
        key: "check",
        render: (_, show: Show) => (
            <div style={{marginLeft: "10px", marginRight: "10px"}}>
                {show.performers
                    .map((performer: Member) => performer.user.id)
                    .includes(user.id) ? (<Button
                    size="small"
                    style={{
                        paddingLeft: "5px", paddingRight: "5px",
                    }}
                    type="primary"
                    onClick={() => removeFromShowRoster(show.id)}
                    disabled={!show.isOpen}
                >
                    <StarFilled/>
                </Button>) : show.isOpen ? (<Button
                    size="small"
                    style={{
                        paddingLeft: "5px", paddingRight: "5px",
                    }}
                    onClick={() => addToShowRoster(show.id)}
                >
                    <PlusOutlined/>
                </Button>) : null}
            </div>),
        width: "2%",
    }, {
        title: (<span
            style={{
                textAlign: "center", width: "100%", display: "inline-block",
            }}
        >
					Priority
				</span>),
        dataIndex: "priority",
        key: "priority",
        render: (priority: number, show: Show) => {
            return (
                <Tag
                    color={!show.isOpen ? "purple" : priority == 0 ? "geekblue" : priority == 1 ? "green" : "red"}
                    key={priority}
                    style={{
                        width: "5.5em",
                        textAlign: "center",
                        cursor: "default"
                    }}
                >
                    {(!show.isOpen ? "closed" : showPriorityChoices[priority] ?? priority).toUpperCase()}
                </Tag>);
        },
        width: "4%",
    }, {
        title: "Show Name",
        dataIndex: "name",
        key: "name",
        render: (name: string, show: Show) => {
            return (<>
                <span style={{fontSize: "1.05em"}}>{name}</span>
                {show.isPending && <Tooltip
                    title="Show pending confirmation"
                    placement="bottom"
                    style={{textAlign: "center"}}
                >
                    <WarningFilled
                        style={{
                            marginLeft: "8px",
                            color: "#faad14"
                        }}
                    />
                </Tooltip>}
                <Tooltip
                    title="More Info"
                    placement="bottom"
                    style={{textAlign: "center"}}
                >
                    <InfoCircleOutlined
                        style={{marginLeft: "5px", color: "gray"}}
                        onClick={() => {
                            Modal.info({
                                content: <ShowDetails show={show}/>,
                                width: "80%",
                            });
                        }}
                    />
                </Tooltip>
            </>);
        },
    }, {
        title: "Date",
        dataIndex: "date",
        key: "date",
        render: (date: string) => (date ? dayjs(date).format("ddd, MMM DD") : ""),
        sorter: (a, b) => a.date.localeCompare(b.date),
    }, {
        title: "Time",
        dataIndex: "rounds",
        key: "rounds",
        render: (rounds: Round[]) => rounds.map(({id, time}: Round) => (
            <div key={id}>
                {time ? dayjs(time, "HH:mm:ss").format("h:mm A") : ""}
            </div>)),
        sorter: (a, b) => a.time?.localeCompare(b.time),
    }, {
        title: (<span
            style={{
                textAlign: "center", width: "100%", display: "inline-block",
            }}
        >
					Lions
				</span>),
        dataIndex: "lions",
        key: "lions",
        width: "5%",
        render: (lions: number) => (<span
            style={{
                textAlign: "center", width: "100%", display: "inline-block",
            }}
        >
					{lions}
				</span>),
    },

        {
            title: "Contact",
            dataIndex: "contact",
            key: "contact",
            render: (contact: Contact) => contact && (<>
                <Tooltip
                    title={contact.phone ? contact.phone.replace(/(\+1)(\d{3})(\d{3})(\d{4})/, "($2) $3-$4") : contact.email ? contact.email : null}
                    placement="bottom"
                    style={{textAlign: "center"}}
                >
                    <Tag
                        icon={contact.phone ? (
                            <PhoneTwoTone/>) : contact.email ? (
                            <MailTwoTone/>) : null}
                        style={{cursor: "pointer"}}
                        color="blue"
                        onClick={async () => {
                            if (contact.phone) {
                                await navigator.clipboard.writeText(contact.phone);
                                await message.info("Phone number copied to clipboard");
                            } else if (contact.email) {
                                await navigator.clipboard.writeText(contact.email);
                                await message.info("Email address copied to clipboard");
                            }
                        }}
                    >
                        {contact.firstName} {contact.lastName}
                    </Tag>
                </Tooltip>
            </>),
        }, {
            title: (<span>
					{"Tentative Roster"}
                <Tooltip title="Final confirmations via Slack"
                         placement="right">
						<InfoCircleTwoTone
                            style={{marginLeft: "6px", fontSize: "0.85em"}}
                        />
					</Tooltip>
				</span>),
            dataIndex: "performers",
            key: "performers",
            render: (performers: Member[], show: Show) => (
                <div style={{display: "flex", justifyContent: "space-between"}}>
                    <Space wrap>
                        {performers
                            .slice()
                            .sort((a: Member, b: Member) => {
                                return a.user.id === show.point?.user.id ? -1 : b.user.id === show.point?.user.id ? 1 : a.user.firstName.localeCompare(b.user.firstName);
                            })
                            .map((performer: Member) => (
                                <Tooltip
                                    title={`${performer.user.firstName} ${performer.user.lastName}`}
                                    placement="bottom"
                                    key={performer.user.id}
                                >
                                    <Tag
                                        style={{
                                            marginRight: "0px",
                                            cursor: "default"
                                        }}
                                        color={performer.user.id === show.point?.user.id ? "volcano" : null}
                                    >
                                        {performer.user.firstName}
                                    </Tag>
                                </Tooltip>))}
                    </Space>
                    <Tooltip
                        title={show.lions ? `${performers.length} of ${performersNeeded(show)} performers` : `${performers.length} performer${performers.length == 1 ? "" : "s"}`}
                        placement="bottom"
                    >
                        <Progress
                            type="circle"
                            percent={show.lions == null ? 0 : Math.round((performers.length / performersNeeded(show)) * 100)}
                            format={() => `${performers.length}`}
                            width={32}
                            style={{
                                marginLeft: "auto",
                                marginRight: "10px",
                                marginTop: "auto",
                                marginBottom: "auto",
                                paddingLeft: "10px",
                                cursor: "default",
                            }}
                        />
                    </Tooltip>
                </div>),
            width: "35%",
        },];

    const isPerforming = (show: Show) => {
        for (const performer of show.performers) {
            if (performer.user.id === user.id) return true;
        }
        return false;
    };

    return <Table
        columns={columns}
        dataSource={
            openFilter === OPTIONS_ENUM.ALL
                ? shows
                : openFilter === OPTIONS_ENUM.MINE
                    ? shows.filter((show: Show) => isPerforming(show))
                    : openFilter === OPTIONS_ENUM.OPEN
                        ? shows.filter((show: Show) => show.isOpen)
                        : shows.filter((show: Show) => !show.isOpen)
        }
        rowKey="id"
        size="middle"
        loading={needsRefresh}
        pagination={false}
    />;
};

export default ShowsTable;
