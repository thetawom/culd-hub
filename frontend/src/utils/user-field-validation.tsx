import {Rule} from "antd/lib/form";

export const FIRST_NAME_VALIDATION_RULES: Rule[] = [
    {
        required: true,
        message: "Please enter your first name."
    },
];

export const LAST_NAME_VALIDATION_RULES: Rule[] = [
    {
        required: true,
        message: "Please enter your last name."
    },
];

export const EMAIL_VALIDATION_RULES: Rule[] = [
    {
        type: "email",
        message: "This is not a valid email address."
    },
    {
        required: true,
        message: "Please enter your email address."
    },
];

export const PHONE_VALIDATION_RULES: Rule[] = [
    {
        pattern: new RegExp(/(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$/g),
        message: "This is not a valid phone number.",
    },
];

export const PASSWORD_VALIDATION_RULES: Rule[] = [
    {
        required: true,
        message: "Please enter your password."
    }
];
