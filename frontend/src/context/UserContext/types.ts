export type User = {
    id: number,
    firstName: string,
    lastName: string,
    email: string,
    phone: string
    member: Member
}

export type Member = {
    school: string;
    classYear: string;
}