import React from "react";
import { Badge, Button, Space, Table, Tag, Tooltip } from "antd";
import {
	PlusOutlined,
	CarTwoTone,
	PhoneTwoTone,
	FireOutlined,
} from "@ant-design/icons";
import dayjs from "dayjs";

var customParseFormat = require("dayjs/plugin/customParseFormat");
dayjs.extend(customParseFormat);

const ShowsTable = ({ shows, user }) => {
	const columns = [
		{
			title: "",
			key: "check",
			render: () => (
				<div style={{ textAlign: "center" }}>
					<Button size="small">
						<PlusOutlined />
					</Button>
				</div>
			),
			width: "2%",
		},
		{
			title: "Priority",
			dataIndex: "priority",
			key: "priority",
			render: (priority) => {
				let [color, text] =
					priority === "A_1"
						? ["blue", "FULL"]
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
			render: (name, { address, contact }) => {
				return (
					<>
						<span>{name}</span>
						<Tooltip
							title={address}
							placement="bottom"
							style={{ textAlign: "center" }}
						>
							<a
								href={`https://www.google.com/maps/search/?api=1&query=${address.replace(
									" ",
									"+"
								)}`}
								target="_blank"
								rel="noreferrer"
							>
								<CarTwoTone style={{ marginLeft: "10px" }} />
							</a>
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
			dataIndex: "time",
			key: "time",
			render: (time) => (time ? dayjs(time, "HH:mm:ss").format("h:mm A") : ""),
			sorter: (a, b) => a.time.localeCompare(b.time),
		},
		{
			title: "Lions",
			dataIndex: "lions",
			key: "lions",
			width: "3%",
			sorter: (a, b) => a.lions - b.lions,
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
			title: "Tentative Roster",
			dataIndex: "performers",
			key: "performers",
			render: (performers, { point }) => (
				<Space>
					{performers.map((performer) => (
						<Tooltip
							title={`${performer.user.firstName} ${performer.user.lastName}`}
							placement="bottom"
							trigger="click"
						>
							{performer.user.id === point?.user.id ? (
								<Badge
									count={
										<FireOutlined
											style={{
												color: "#f5222d",
												fontSize: "0.8em",
											}}
										/>
									}
								>
									<Tag style={{ marginRight: "0px", cursor: "pointer" }}>
										{performer.user.firstName}
									</Tag>
								</Badge>
							) : (
								<Tag style={{ marginRight: "0px", cursor: "pointer" }}>
									{performer.user.firstName}
								</Tag>
							)}
						</Tooltip>
					))}
				</Space>
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
							title={contact.phone.replace(
								/(\+1)(\d{3})(\d{3})(\d{4})/,
								"($2) $3-$4"
							)}
							placement="bottom"
							style={{ textAlign: "center" }}
						>
							<Tag icon={<PhoneTwoTone />} style={{ cursor: "pointer" }}>
								{contact.firstName} {contact.lastName}
							</Tag>
						</Tooltip>
					</>
				),
		},
	];

	return <Table columns={columns} dataSource={shows} rowKey="id" />;
};

export default ShowsTable;
