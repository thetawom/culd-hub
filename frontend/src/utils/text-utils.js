export const toLowerCase = (str) => (str || "").toLowerCase();

export const toTitleCase = (str) => str && str.toLowerCase().replace(/^(.)|\s(.)/g, function ($1) {
    return $1.toUpperCase();
});