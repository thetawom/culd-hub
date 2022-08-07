export const firstNameValidationRules = [{required: true, message: "Please enter your first name."},];

export const lastNameValidationRules = [{required: true, message: "Please enter your last name."},];

export const emailValidationRules = [{type: "email", message: "This is not a valid email address."}, {
    required: true, message: "Please enter your email address."
},];

export const phoneValidationRules = [{
    pattern: new RegExp(/(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$/g),
    message: "This is not a valid phone number.",
},];

