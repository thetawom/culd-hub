import React, {useContext} from "react";
import {Badge, BadgeProps, Calendar, Modal, Typography} from "antd";
import dayjs, {Dayjs} from "dayjs";
import {ShowContextInterface} from "../../context/ShowsTableContext/types";
import ShowsTableContext from "../../context/ShowsTableContext";
import {Views} from "../ShowsTableControls";
import ShowDetails from "../ShowDetails";

const ShowCalendar = () => {

    const {
        shows,
        view
    }: ShowContextInterface = useContext(ShowsTableContext);

    type TimeUnit = "day" | "month";

    const getShowDataForDate = (date: Dayjs, unit: TimeUnit) => {
        const listData = shows
            .filter(show => dayjs(show.date).isSame(date, unit))
            .map(show => ({
                type: show.isOpen ? (show.isPending ? "warning" : "success") : "default",
                content: show.name,
                details: <ShowDetails show={show}/>,
            }));
        return listData || [];
    };

    const cellRender = (unit: TimeUnit) => {
        const render = (date: Dayjs) => {
            const listData = getShowDataForDate(date, unit);
            return (
                <ul style={{listStyleType: "none", margin: 0, padding: 0}}>
                    {listData.map((item) => (
                        <Typography.Paragraph
                            ellipsis key={item.content}
                            style={{marginBottom: 0}}
                            onClick={() => {
                                Modal.info({
                                    title: item.content,
                                    content: item.details,
                                    width: "60%",
                                });
                            }}>
                            <Badge
                                status={item.type as BadgeProps["status"]}
                                text={item.content}
                            />
                        </Typography.Paragraph>
                    ))}
                </ul>
            );
        };
        return render;
    };

    return view == Views.CALENDAR && <Calendar
        dateCellRender={cellRender("day")}
        monthCellRender={cellRender("month")}
        validRange={[dayjs("2022-09-01"), dayjs("2023-05-31")]}
        style={{padding: "10px 25px"}}
    />;
};

export default ShowCalendar;