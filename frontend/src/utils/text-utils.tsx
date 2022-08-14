export const toLowerCase = (str: string): string =>
    (str || "").toLowerCase();

export const toTitleCase = (str: string): string =>
    str && str.toLowerCase().replace(/^(.)|\s(.)/g,
        ($1) => $1.toUpperCase()
    );