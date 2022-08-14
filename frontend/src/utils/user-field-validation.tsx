import {Rule} from "antd/lib/form";

export const firstNameValidationRules: Rule[] = [
    {
        required: true,
        message: "Please enter your first name."
    },
];

export const lastNameValidationRules: Rule[] = [
    {
        required: true,
        message: "Please enter your last name."
    },
];

export const emailValidationRules: Rule[] = [
    {
        type: "email",
        message: "This is not a valid email address."
    },
    {
        required: true,
        message: "Please enter your email address."
    },
];

export const phoneValidationRules: Rule[] = [
    {
        pattern: new RegExp(/(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$/g),
        message: "This is not a valid phone number.",
    },
];

