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
    GET_POSITION_CHOICES_QUERY,
    GET_SCHOOL_CHOICES_QUERY
} from "./queries";
import Loader from "../../components/Loader";


const ProfilePage = () => {

    const {user} = useContext(UserContext);
    const [schoolChoices, setSchoolChoices] = useState(null);
    const [classYearChoices, setClassYearChoices] = useState(null);
    const [positionChoices, setPositionChoices] = useState(null);

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

    const {loading: positionChoicesLoading}: QueryResult = useAuthQuery(GET_POSITION_CHOICES_QUERY, {
        onCompleted: ({positionChoices}: { positionChoices: string }) => {
            setPositionChoices(JSON.parse(positionChoices));
        },
    });

    const isLoading: boolean = classYearChoicesLoading || schoolChoicesLoading || positionChoicesLoading
        || !classYearChoices || !schoolChoices || !positionChoices;

    return <Layout>
        <Header/>
        <Layout.Content className={styles.content}>
            <Row className={styles.heading} justify="space-between"
                 align="bottom">
                <Typography.Title className={styles.title} level={2}>
                    <SmileOutlined className={styles.icon}/>Member Profile
                </Typography.Title>
                <Typography className={styles.subtitle}>
                    {positionChoices ? positionChoices[user.member.position] : ""}
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
                                       noStyle
                                       initialValue={user.member.school}>
                                <Select placeholder="School"
                                        className={styles.fullWidthInput}
                                        options={Object.entries(schoolChoices).map(([key, value]) => ({
                                            label: value.toString(),
                                            value: parseInt(key)
                                        }))}/>
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
                                       noStyle
                                       initialValue={user.member.classYear}>
                                <Select placeholder="Class year"
                                        className={styles.fullWidthInput}
                                        options={Object.entries(classYearChoices).map(([key, value]) => ({
                                            label: value.toString(),
                                            value: parseInt(key)
                                        }))}/>
                            </Form.Item>
                        }
                    />
                </Space>}
        </Layout.Content>
    </Layout>;
};

export default ProfilePage;