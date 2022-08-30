export type User = {
    id: number,
    firstName: string,
    lastName: string,
    email: string,
    phone: string
    member: Member
}

export type Member = {
    user: User,
    school: string,
    classYear: string
}

export type Show = {
    id: number,
    name: string,
    priority: string,
    date: string,
    time: string,
    rounds: Round[],
    address: string,
    lions: number,
    performers: Member[],
    point: Member,
    contact: Contact,
    isCampus: boolean,
    isOpen: boolean,
}

export type Round = {
    id: number,
    time: string
}

export type Contact = {
    firstName: string,
    lastName: string,
    phone: string,
    email: string
}