const grabStoredCookie = (cookieKey: string): string => {
    const cookies: { [key: string]: string } = document.cookie
        .split('; ')
        .reduce((prev: { [key: string]: string }, current) => {
            const [key, ...value] = current.split('=')
            prev[key] = value.join('=')
            return prev
        }, {})
    const cookieVal = cookieKey in cookies ? cookies[cookieKey] : ''
    return cookieVal
}

const delay = (ms: number): Promise<void> => {
    return new Promise((resolve) => setTimeout(resolve, ms))
}

export { grabStoredCookie, delay }
