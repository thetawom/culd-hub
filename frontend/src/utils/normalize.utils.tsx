import parsePhoneNumber from "libphonenumber-js";

export const toLowerCase = (str: string): string =>
    (str || "").toLowerCase();

export const toTitleCase = (str: string): string =>
    str && str.toLowerCase().replace(/^(.)|\s(.)/g,
        ($1) => $1.toUpperCase()
    );

export const formatPhoneNumber = (str: string): string => {
    const phoneNumber = parsePhoneNumber(str);
    return (phoneNumber.country === "US") ? phoneNumber.formatNational() : phoneNumber.formatInternational();
};