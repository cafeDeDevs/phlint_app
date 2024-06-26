import { useNavigate } from 'react-router-dom'
import { useState } from 'react'

import { delay } from '../utils/'

const AuthPage = () => {
    const navigate = useNavigate()
    const [errorMsg, setErrorMsg] = useState<string | null>(null)
    const [successMsg, setSuccessMsg] = useState<string | null>(null)

    const logout = async () => {
        try {
            const res = await fetch(import.meta.env.VITE_BACKEND_LOGOUT_ROUTE, {
                method: 'POST',
                headers: {
                    Accept: 'application/json',
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
            })

            if (!res.ok) {
                const jsonRes = await res.json()
                throw new Error(jsonRes.mesage)
            }
            setSuccessMsg(
                'You Have Successfully Logged Out! \nRedirecting you back home!',
            )
            await delay(3000)
            navigate('/')
        } catch (err) {
            if (err instanceof Error) {
                console.error('ERROR :=>', err.message)
                setErrorMsg(err.message)
            }
        }
    }

    return (
        <>
            {!successMsg && (
                <>
                    <div>Congratulations! You Are Authenticated!</div>
                    <button type='button' onClick={logout}>
                        Logout
                    </button>
                </>
            )}
            {successMsg && <p>{successMsg}</p>}
            {errorMsg && <p>{errorMsg}</p>}
        </>
    )
}

export default AuthPage
