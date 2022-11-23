import {Descriptions, message, Space, Tag, Tooltip} from "antd";
import dayjs from "dayjs";
import React from "react";
import {Member, Show} from "../../../../types/types";
import {
    InfoCircleTwoTone,
    MailOutlined,
    PhoneOutlined
} from "@ant-design/icons";

const ShowDetails = ({show}: { show: Show }) => {
    return (
        <Descriptions layout="vertical" bordered size="middle">
            <Descriptions.Item label="Date">
                {show.date.format("ddd, MMM DD") || "TBD"}
            </Descriptions.Item>
            <Descriptions.Item label="Time(s)">
                <Space>
                    {show.rounds?.map((round, i) =>
                        <span
                            key={i}>{dayjs(round.time, "HH:mm:ss").format("h:mm A")}</span>)}
                </Space>
            </Descriptions.Item>
            <Descriptions.Item label="Address">
                {show.address || "TBD"}
            </Descriptions.Item>
            <Descriptions.Item label="Point Person">
                {show.point ? <Tag style={{cursor: "default"}}>
                    {`${show.point.user.firstName} ${show.point.user.lastName}`}
                </Tag> : ""}
            </Descriptions.Item>
            <Descriptions.Item label="Lions">
                {show.lions || ""}
            </Descriptions.Item>
            <Descriptions.Item label="Contact Information">
                {show.contact ? <Space wrap size={0}>
                    <Tag>{`${show.contact.firstName} ${show.contact.lastName}`}</Tag>
                    {show.contact.phone && <Tag
                        icon={<PhoneOutlined/>}
                        style={{cursor: "pointer"}}
                        onClick={async () => {
                            await navigator.clipboard.writeText(show.contact.phone);
                            await message.info("Phone number copied to clipboard");
                        }}
                    >
                        {show.contact.phone.replace(/(\+1)(\d{3})(\d{3})(\d{4})/, "($2) $3-$4")}
                    </Tag>}
                    {show.contact.email && <Tag
                        icon={<MailOutlined/>}
                        style={{cursor: "pointer"}}
                        onClick={async () => {
                            await navigator.clipboard.writeText(show.contact.email);
                            await message.info("Email address copied to clipboard");
                        }}
                    >
                        {show.contact.email}
                    </Tag>}
                </Space> : "TBD"}
            </Descriptions.Item>


            <Descriptions.Item label={<>{"Tentative Roster"}<Tooltip
                title="Final confirmations via Slack"
                placement="right">
                <InfoCircleTwoTone
                    style={{marginLeft: "6px", fontSize: "0.85em"}}
                />
            </Tooltip></>}>
                <Space wrap>
                    {show.performers
                        .slice()
                        .map((performer: Member) => (
                            <Tag
                                key={performer.user.id}
                                style={{
                                    marginRight: "0px",
                                    cursor: "default"
                                }}
                            >
                                {`${performer.user.firstName} ${performer.user.lastName}`}
                            </Tag>
                        ))}
                </Space>
            </Descriptions.Item>
        </Descriptions>
    );
};

export default ShowDetails;