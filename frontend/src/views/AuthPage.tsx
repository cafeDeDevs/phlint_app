import { useNavigate } from 'react-router-dom'
import { useEffect, useState } from 'react'

import { delay } from '../utils/'

const AuthPage = () => {
    const navigate = useNavigate()
    useEffect(() => {
        const redirectToGallery = async () => {
            await delay(3000)
            navigate('/gallery')
        }
        redirectToGallery()
    }, [])

    /* TODO: Move this into it's own component in the nav bar
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
    */

    return (
        <>
            <>
                <div>Congratulations! You Are Authenticated!</div>
                <div>One Moment While We Redirect You To Your Gallery!...</div>
                {/*  TODO: Move this into it's own component in the nav bar
                    <button type='button' onClick={logout}>
                        Logout
                    </button>
                    */}
            </>
            {/* 
            {successMsg && <p>{successMsg}</p>}
            {errorMsg && <p>{errorMsg}</p>}

                */}
        </>
    )
}

export default AuthPage
