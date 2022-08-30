export interface APIInterface {
    success: boolean;
    errors: Record<string, APIError[]>;
}

type APIError = {
    message: string,
    code: string
}