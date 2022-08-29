export interface APIInterface {
    success: boolean;
    errors: Record<string, APIError[]>;
}

export type APIError = {
    message: string,
    code: string
}

export type UserType = {
    id: number,
    firstName: string,
    lastName: string,
    email: string,
    phone: string
}