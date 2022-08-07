import React, {useContext, useState} from "react";
import {Divider, Form, Input, Layout, Select, Space, Typography} from "antd";
import {SmileOutlined} from "@ant-design/icons";
import UserContext from "../context/UserContext";
import Header from "../components/Header";
import ProfileItem from "../components/ProfileItem";
import {gql} from "@apollo/client";
import Loader from "../components/Loader";
import useAuthQuery from "../utils/useAuthQuery";


const GET_SCHOOL_CHOICES_QUERY = gql`
	{
		schoolChoices
	}
`;

const GET_CLASS_YEAR_CHOICES_QUERY = gql`
	{
		classYearChoices
	}
`;

const GET_MEMBERSHIP_CHOICES_QUERY = gql`
    {
        membershipChoices
    }
`;

const ProfilePage = () => {
    let {user} = useContext(UserContext);
    let [schoolChoices, setSchoolChoices] = useState(null);
    let [classYearChoices, setClassYearChoices] = useState(null);
    let [membershipChoices, setMembershipChoices] = useState(null);

    let {schoolChoicesLoading} = useAuthQuery(GET_SCHOOL_CHOICES_QUERY, {
        onCompleted: ({schoolChoices}) => {
            setSchoolChoices(JSON.parse(schoolChoices));
        },
    });

    let {classYearChoicesLoading} = useAuthQuery(GET_CLASS_YEAR_CHOICES_QUERY, {
        onCompleted: ({classYearChoices}) => {
            setClassYearChoices(JSON.parse(classYearChoices));
        },
    });

    let {membershipChoicesLoading} = useAuthQuery(GET_MEMBERSHIP_CHOICES_QUERY, {
        onCompleted: ({membershipChoices}) => {
            setMembershipChoices(JSON.parse(membershipChoices));
        },
    });

    console.log(user.member);

    return classYearChoicesLoading || !classYearChoices ||
    schoolChoicesLoading || !schoolChoices ? (
        <Loader/>
    ) : (
        <Layout style={{minHeight: "100vh"}}>
            <Header/>
            <Layout.Content
                id="profile-page"
                style={{
                    width: "40%",
                    margin: "auto",
                    padding: "30px",
                }}
            >
                <Space align="baseline" style={{width: "100%", justifyContent: "space-between"}}>
                    <Typography.Title level={2} style={{marginBottom: "0em"}}>
                        <SmileOutlined
                            style={{
                                fontSize: "0.9em",
                                marginRight: "0.4em",
                            }}
                        />
                        Member Profile
                    </Typography.Title>
                    <Typography style={{color: "gray"}}>
                        {membershipChoices ? membershipChoices[user.member.membership] : ""}
                    </Typography>
                </Space>
                <Divider style={{marginTop: "0.8em", marginBottom: "1.2em"}}/>
                <Space style={{width: "100%"}} direction="vertical">
                    <ProfileItem
                        title="Full Name"
                        value={`${user.firstName} ${user.lastName}`}
                        input={
                            <Input.Group compact style={{width: "calc(100% - 50px)"}}>
                                <Form.Item name="firstName" initialValue={user.firstName} noStyle>
                                    <Input placeholder="First name" style={{width: "50%"}}/>
                                </Form.Item>
                                <Form.Item name="lastName" initialValue={user.lastName} noStyle>
                                    <Input placeholder="Last name" style={{width: "50%"}}/>
                                </Form.Item>
                            </Input.Group>
                        }
                    />
                    <ProfileItem
                        title="Email Address"
                        value={user.email}
                        input={
                            <Form.Item name="email" initialValue={user.email} noStyle>
                                <Input placeholder="Email address" style={{width: "calc(100% - 50px)"}}/>
                            </Form.Item>
                        }
                    />
                    <ProfileItem
                        title="Phone Number"
                        value={user.phone || "Not set"}
                        input={
                            <Form.Item name="phone" initialValue={user.phone} noStyle>
                                <Input placeholder="Phone number" style={{width: "calc(100% - 50px)"}}/>
                            </Form.Item>
                        }
                    />
                    <ProfileItem
                        title="School"
                        value={user.member.school || "Not set"}
                        choices={schoolChoices}
                        input={
                            <Form.Item name="school" initialValue={user.member.school} noStyle>
                                <Select placeholder="School" style={{width: "calc(100% - 50px)"}}>
                                    <>
                                        {Object.entries(schoolChoices).map(([key, value]) =>
                                            <Select.Option key={key} value={key}>{value.toString()}</Select.Option>
                                        )}
                                    </>
                                </Select>
                            </Form.Item>
                        }
                    />
                    <ProfileItem
                        title="Class Year"
                        value={user.member.classYear || "Not set"}
                        choices={classYearChoices}
                        input={
                            <Form.Item name="classYear" initialValue={user.member.classYear} noStyle>
                                <Select placeholder="Class year" style={{width: "calc(100% - 50px)"}}>
                                    <>
                                        {Object.entries(classYearChoices).map(([key, value]) =>
                                            <Select.Option key={key} value={key}>{value.toString()}</Select.Option>
                                        )}
                                    </>
                                </Select>
                            </Form.Item>
                        }
                    />
                </Space>
            </Layout.Content>
        </Layout>
    );
};

export default ProfilePage;