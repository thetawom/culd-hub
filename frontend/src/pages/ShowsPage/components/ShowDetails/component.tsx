import {Descriptions, Space} from "antd";
import dayjs from "dayjs";
import React from "react";
import {Show} from "../../../../types/types";

const ShowDetails = ({show}: { show: Show }) => {
    return (
        <Descriptions title={show.name} layout="vertical" bordered>
            <Descriptions.Item label="Address">
                {show.address || ""}
            </Descriptions.Item>
            <Descriptions.Item label="Date">
                {show.date || ""}
            </Descriptions.Item>
            <Descriptions.Item label="Time(s)">
                <Space>
                    {show.rounds?.map((round, i) =>
                        <span
                            key={i}>{dayjs(round.time, "HH:mm:ss").format("h:mm A")}</span>)}
                </Space>
            </Descriptions.Item>
            <Descriptions.Item label="Contact Information">
                <p>{show.contact ? `Name: ${show.contact.firstName} ${show.contact.lastName}` : ""}</p>
                <p>{show.contact ? show.contact.phone && `Phone: ${show.contact.phone}` : ""}</p>
                <p>{show.contact ? show.contact.email && `Email: ${show.contact.email}` : ""}</p>
            </Descriptions.Item>
            <Descriptions.Item label="Point Person">
                {`${show.point?.user.firstName} ${show.point?.user.lastName}`}
            </Descriptions.Item>
            <Descriptions.Item label="Number of Lions">
                {show.lions || ""}
            </Descriptions.Item>
            <Descriptions.Item label="Tentative Roster">
                <Space>
                    {show.performers?.map((item, i) =>
                            <span
                                key={i}>{`${item.user.firstName} ${item.user.lastName}`}
                    </span>
                    )}
                </Space>
            </Descriptions.Item>
        </Descriptions>
    );
};

export default ShowDetails;