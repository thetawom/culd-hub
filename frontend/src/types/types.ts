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
    school: number,
    classYear: number,
    position: number,
}

export type Show = {
    id: number,
    name: string,
    priority: number,
    date: string,
    time: string,
    rounds: Round[],
    address: string,
    lions: number,
    performers: Member[],
    point: Member,
    contact: Contact,
    isCampus: boolean,
    isOutOfCity: boolean,
    isOpen: boolean,
    isPending: boolean,
    status: number,
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