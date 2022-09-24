import React, {useContext, useState} from "react";
import {
    Divider,
    Form,
    Input,
    Layout,
    Row,
    Select,
    Space,
    Typography
} from "antd";
import {
    MailOutlined,
    PhoneOutlined,
    SmileOutlined,
    UserOutlined
} from "@ant-design/icons";
import {UserContext} from "../../context/UserContext";
import Header from "../../components/Header";
import ProfileItem from "./components/ProfileItem";
import {QueryResult, useAuthQuery} from "../../services/graphql";
import {
    EMAIL_VALIDATION_RULES,
    FIRST_NAME_VALIDATION_RULES,
    formatPhoneNumber,
    LAST_NAME_VALIDATION_RULES,
    PHONE_VALIDATION_RULES,
    toLowerCase,
    toTitleCase
} from "../../services/validation";
import styles from "./style.module.css";
import {
    GET_CLASS_YEAR_CHOICES_QUERY,
    GET_MEMBERSHIP_CHOICES_QUERY,
    GET_SCHOOL_CHOICES_QUERY
} from "./queries";
import Loader from "../../components/Loader";


const ProfilePage = () => {

    const {user} = useContext(UserContext);
    const [schoolChoices, setSchoolChoices] = useState(null);
    const [classYearChoices, setClassYearChoices] = useState(null);
    const [membershipChoices, setMembershipChoices] = useState(null);

    const {loading: schoolChoicesLoading}: QueryResult = useAuthQuery(GET_SCHOOL_CHOICES_QUERY, {
        onCompleted: ({schoolChoices}: { schoolChoices: string }) => {
            setSchoolChoices(JSON.parse(schoolChoices));
        },
    });

    const {loading: classYearChoicesLoading}: QueryResult = useAuthQuery(GET_CLASS_YEAR_CHOICES_QUERY, {
        onCompleted: ({classYearChoices}: { classYearChoices: string }) => {
            setClassYearChoices(JSON.parse(classYearChoices));
        },
    });

    const {loading: membershipChoicesLoading}: QueryResult = useAuthQuery(GET_MEMBERSHIP_CHOICES_QUERY, {
        onCompleted: ({membershipChoices}: { membershipChoices: string }) => {
            setMembershipChoices(JSON.parse(membershipChoices));
        },
    });

    const isLoading: boolean = classYearChoicesLoading || schoolChoicesLoading || membershipChoicesLoading
        || !classYearChoices || !schoolChoices || !membershipChoices;

    return <Layout>
        <Header/>
        <Layout.Content className={styles.content}>
            <Row className={styles.heading} justify="space-between"
                 align="bottom">
                <Typography.Title className={styles.title} level={2}>
                    <SmileOutlined className={styles.icon}/>Member Profile
                </Typography.Title>
                <Typography className={styles.subtitle}>
                    {membershipChoices ? membershipChoices[user.member.membership] : ""}
                </Typography>
            </Row>
            <Divider className={styles.divider}/>
            {isLoading ? <Loader/> :
                <Space className={styles.profileItemSpace} direction="vertical">
                    <ProfileItem
                        title="Full Name"
                        values={{
                            firstName: user.firstName,
                            lastName: user.lastName
                        }}
                        display={values => `${values.firstName} ${values.lastName}`}
                        input={
                            <Input.Group compact
                                         className={styles.fullWidthInput}>
                                <Form.Item
                                    name="firstName"
                                    initialValue={user.firstName}
                                    rules={FIRST_NAME_VALIDATION_RULES}
                                    normalize={toTitleCase}
                                    noStyle>
                                    <Input placeholder="First name"
                                           className={styles.halfWidthInput}
                                           prefix={<UserOutlined/>}/>
                                </Form.Item>
                                <Form.Item
                                    name="lastName"
                                    initialValue={user.lastName}
                                    rules={LAST_NAME_VALIDATION_RULES}
                                    normalize={toTitleCase}
                                    noStyle>
                                    <Input placeholder="Last name"
                                           className={styles.halfWidthInput}/>
                                </Form.Item>
                            </Input.Group>
                        }
                    />
                    <ProfileItem
                        title="Email Address"
                        values={{email: user.email}}
                        display={values => values.email}
                        input={
                            <Form.Item
                                name="email"
                                initialValue={user.email}
                                rules={EMAIL_VALIDATION_RULES}
                                normalize={toLowerCase}
                                noStyle>
                                <Input placeholder="Email address"
                                       className={styles.fullWidthInput}
                                       prefix={<MailOutlined/>}/>
                            </Form.Item>
                        }
                    />
                    <ProfileItem
                        title="Phone Number"
                        values={{phone: user.phone}}
                        display={values => formatPhoneNumber(values.phone) || "Not set"}
                        input={
                            <Form.Item
                                name="phone"
                                initialValue={user.phone}
                                rules={PHONE_VALIDATION_RULES}
                                noStyle>
                                <Input placeholder="Phone number"
                                       className={styles.fullWidthInput}
                                       prefix={<PhoneOutlined/>}/>
                            </Form.Item>
                        }
                    />
                    <ProfileItem
                        title="School"
                        values={{school: user.member.school}}
                        display={values => (values.school != null) ? values.school : "Not set"}
                        choices={schoolChoices}
                        input={
                            <Form.Item name="school"
                                       noStyle>
                                <Select placeholder="School"
                                        className={styles.fullWidthInput}
                                        defaultValue={schoolChoices[user.member.school]}>
                                    <>
                                        {Object.entries(schoolChoices).map(([key, value]) =>
                                            <Select.Option key={key}
                                                           value={key}>{value.toString()}</Select.Option>)}
                                    </>
                                </Select>
                            </Form.Item>
                        }
                    />
                    <ProfileItem
                        title="Class Year"
                        values={{classYear: user.member.classYear}}
                        display={values => values.classYear || "Not set"}
                        choices={classYearChoices}
                        input={
                            <Form.Item name="classYear"
                                       noStyle>
                                <Select placeholder="Class year"
                                        className={styles.fullWidthInput}
                                        defaultValue={classYearChoices[user.member.classYear]}>
                                    <>
                                        {Object.entries(classYearChoices).map(([key, value]) =>
                                            <Select.Option key={key}
                                                           value={key}>{value.toString()}</Select.Option>)}
                                    </>
                                </Select>
                            </Form.Item>
                        }
                    />
                </Space>}
        </Layout.Content>
    </Layout>;
};

export default ProfilePage;