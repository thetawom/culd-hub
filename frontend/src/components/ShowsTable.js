import React, { useContext, useEffect, useState } from "react";
import { message, Button, Space, Table, Tag, Tooltip, Progress } from "antd";
import {
	PlusOutlined,
	CompassTwoTone,
	PhoneTwoTone,
	MailTwoTone,
	StarFilled,
} from "@ant-design/icons";
import dayjs from "dayjs";
import { gql } from "@apollo/client";
import useAuthMutation from "../utils/useAuthMutation";
import AuthContext from "../context/AuthContext";
import useAuthLazyQuery from "../utils/useAuthLazyQuery";
import Loader from "./Loader";

var customParseFormat = require("dayjs/plugin/customParseFormat");
dayjs.extend(customParseFormat);

const GET_SHOWS_QUERY = gql`
	{
		shows {
			id
			name
			priority
			date
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

const ShowsTable = ({ user, openFilter, refreshed, setRefreshed }) => {
	let { logoutUser } = useContext(AuthContext);

	let [shows, setShows] = useState([]);

	let [getShows] = useAuthLazyQuery(GET_SHOWS_QUERY, {
		onCompleted: ({ shows }) => {
			setShows(shows);
			setRefreshed(true);
		},
		onError: () => logoutUser(),
		fetchPolicy: "network-only",
		nextFetchPolicy: "network-only",
	});

	useEffect(() => {
		getShows();
	}, [refreshed, getShows]);

	let [createRole] = useAuthMutation(CREATE_ROLE_MUTATION, {
		onCompleted: ({ createRole }) => {
			setShows(
				shows.map((show) =>
					show.id === createRole.role.show.id
						? {
								...show,
								performers: [...show.performers, createRole.role.performer],
						  }
						: { ...show }
				)
			);
			message.success(`Signed up for ${createRole.role.show.name}`);
		},
		onError: (error) => {
			console.log(error.message);
		},
	});

	let addSignup = (id, isOpen) => {
		if (isOpen) {
			createRole({
				variables: {
					showId: id,
				},
			});
		} else {
			message.error(
				"At this point, the roster has been finalized. Please contact an E-Board member to be added to the roster."
			);
		}
	};

	let [deleteRole] = useAuthMutation(DELETE_ROLE_MUTATION, {
		onCompleted: ({ deleteRole }) => {
			setShows(
				shows.map((show) =>
					show.id === deleteRole.role.show.id
						? {
								...show,
								performers: show.performers.filter(
									(performer) =>
										performer.user.id !== deleteRole.role.performer.user.id
								),
						  }
						: { ...show }
				)
			);
			message.success(`Removed from ${deleteRole.role.show.name}`);
		},
		onError: (error) => {
			console.log(error.message);
		},
	});

	let removeSignup = (id, isOpen) => {
		if (isOpen) {
			deleteRole({
				variables: {
					showId: id,
				},
			});
		} else {
			message.error(
				"Please contact an E-Board member to be removed from this roster."
			);
		}
	};

	const columns = [
		{
			title: "",
			key: "check",
			render: (_, { id, performers, isOpen }) => (
				<div style={{ marginLeft: "10px", marginRight: "10px" }}>
					{performers
						.map((performer) => performer.user.id)
						.includes(user.id) ? (
						<Button
							size="small"
							style={{
								paddingLeft: "5px",
								paddingRight: "5px",
							}}
							type="primary"
							onClick={() => removeSignup(id, isOpen)}
							disabled={!isOpen}
						>
							<StarFilled />
						</Button>
					) : isOpen ? (
						<Button
							size="small"
							style={{
								paddingLeft: "5px",
								paddingRight: "5px",
							}}
							onClick={() => addSignup(id, isOpen)}
						>
							<PlusOutlined />
						</Button>
					) : null}
				</div>
			),
			width: "2%",
		},
		{
			title: (
				<span
					style={{
						textAlign: "center",
						width: "100%",
						display: "inline-block",
					}}
				>
					Priority
				</span>
			),
			dataIndex: "priority",
			key: "priority",
			render: (priority, { isOpen }) => {
				let [color, text] = !isOpen
					? ["purple", "CLOSED"]
					: priority === "A_1"
					? ["geekblue", "FULL"]
					: priority === "A_2"
					? ["green", "NORMAL"]
					: ["red", "URGENT"];
				return (
					<Tag
						color={color}
						key={priority}
						style={{ width: "5.5em", textAlign: "center" }}
					>
						{text}
					</Tag>
				);
			},
			width: "4%",
		},
		{
			title: "Performance",
			dataIndex: "name",
			key: "name",
			render: (name, { address }) => {
				let index = address.search(/(?:^|\D)(\d{5})(?!\d)/g);
				return (
					<>
						<span style={{ fontSize: "1.05em" }}>{name}</span>
						<Tooltip
							title={index < 0 ? address : address.substring(0, index)}
							placement="bottom"
							style={{ textAlign: "center" }}
						>
							<CompassTwoTone
								style={{ marginLeft: "10px" }}
								onClick={() => {
									navigator.clipboard.writeText(address);
									message.info("Address copied to clipboard");
								}}
							/>
						</Tooltip>
					</>
				);
			},
		},
		{
			title: "Date",
			dataIndex: "date",
			key: "date",
			render: (date) => (date ? dayjs(date).format("ddd, MMM DD") : ""),
			sorter: (a, b) => a.date.localeCompare(b.date),
		},
		{
			title: "Time",
			dataIndex: "rounds",
			key: "rounds",
			render: (rounds) =>
				rounds.map(({ id, time }) => (
					<div key={id}>
						{time ? dayjs(time, "HH:mm:ss").format("h:mm A") : ""}
					</div>
				)),
			sorter: (a, b) => a.time.localeCompare(b.time),
		},
		{
			title: (
				<span
					style={{
						textAlign: "center",
						width: "100%",
						display: "inline-block",
					}}
				>
					Lions
				</span>
			),
			dataIndex: "lions",
			key: "lions",
			width: "5%",
			render: (lions) => (
				<span
					style={{
						textAlign: "center",
						width: "100%",
						display: "inline-block",
					}}
				>
					{lions}
				</span>
			),
		},

		{
			title: "Contact",
			dataIndex: "contact",
			key: "contact",
			render: (contact) =>
				contact && (
					<>
						<Tooltip
							title={
								contact.phone
									? contact.phone.replace(
											/(\+1)(\d{3})(\d{3})(\d{4})/,
											"($2) $3-$4"
									  )
									: contact.email
									? contact.email
									: null
							}
							placement="bottom"
							style={{ textAlign: "center" }}
						>
							<Tag
								icon={
									contact.phone ? (
										<PhoneTwoTone />
									) : contact.email ? (
										<MailTwoTone />
									) : null
								}
								style={{ cursor: "pointer" }}
								color="blue"
								onClick={() => {
									if (contact.phone) {
										navigator.clipboard.writeText(contact.phone);
										message.info("Phone number copied to clipboard");
									} else if (contact.email) {
										navigator.clipboard.writeText(contact.email);
										message.info("Email address copied to clipboard");
									}
								}}
							>
								{contact.firstName} {contact.lastName}
							</Tag>
						</Tooltip>
					</>
				),
		},
		{
			title: "Tentative Roster",
			dataIndex: "performers",
			key: "performers",
			render: (performers, { lions, point }) => (
				<div style={{ display: "flex", justifyContent: "space-between" }}>
					<Space>
						{performers
							.slice()
							.sort((a, b) => {
								return a.user.id === point?.user.id
									? -1
									: b.user.id === point?.user.id
									? 1
									: a.user.firstName.localeCompare(b.user.firstName);
							})
							.map((performer) => (
								<Tooltip
									title={`${performer.user.firstName} ${performer.user.lastName}`}
									placement="bottom"
									trigger="click"
									key={performer.user.id}
								>
									<Tag
										style={{ marginRight: "0px", cursor: "pointer" }}
										color={
											performer.user.id === point?.user.id ? "volcano" : null
										}
									>
										{performer.user.firstName}
									</Tag>
								</Tooltip>
							))}
					</Space>
					<Progress
						type="circle"
						percent={Math.round((performers.length / (lions * 2 + 2)) * 100)}
						format={() => `${performers.length}/${lions * 2 + 2}`}
						width={32}
						style={{ marginLeft: "auto", marginRight: "10px" }}
					/>
				</div>
			),
		},
	];

	return refreshed ? (
		<Table
			columns={columns}
			dataSource={
				openFilter === "All"
					? shows
					: openFilter === "Open"
					? shows.filter((show) => show.isOpen)
					: shows.filter((show) => !show.isOpen)
			}
			rowKey="id"
			size="middle"
		/>
	) : (
		<Loader />
	);
};

export default ShowsTable;
