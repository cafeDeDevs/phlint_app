import { useEffect, type ReactNode } from 'react'
import { AuthContext } from './AuthContext'
import { useNavigate } from 'react-router-dom'

import { grabStoredCookie } from '../utils/'
import urls from '../config/urls'

interface Props {
    children?: ReactNode
}

// TODO: Render a page to user explaining if
// authentication failed, to please sign in again
export default function AuthContextProvider({ children }: Props) {
    const navigate = useNavigate()
    useEffect(() => {
        const authenticate = async () => {
            const csrfToken = grabStoredCookie('csrftoken')
            try {
                const testRes = await fetch(urls.BACKEND_TEST_ROUTE, {
                    method: 'POST',
                    headers: {
                        Accept: 'application/json',
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken,
                    },
                    credentials: 'include',
                })
                const jsonRes = await testRes.json()
                if (!testRes.ok) {
                    throw new Error(jsonRes.message)
                }
            } catch (err) {
                console.error('ERROR :=>', err)
                navigate('/')
            }
        }
        authenticate()
    }, [navigate])

    return (
        <AuthContext.Provider value={() => {}}>{children}</AuthContext.Provider>
    )
}
