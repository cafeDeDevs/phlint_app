import '../css/ProfileCard.css'
import { useNavigate } from 'react-router-dom'
import { useState } from 'react'

import { delay } from '../utils/'
import urls from '../config/urls'

const ProfileCard = () => {
    const navigate = useNavigate()
    const [errorMsg, setErrorMsg] = useState<string | null>(null)
    const [successMsg, setSuccessMsg] = useState<string | null>(null)

    const logout = async () => {
        try {
            const res = await fetch(urls.BACKEND_LOGOUT_ROUTE, {
                method: 'POST',
                headers: {
                    Accept: 'application/json',
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
            })

            if (!res.ok) {
                const jsonRes = await res.json()
                throw new Error(jsonRes.message)
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
            <div className='profile-card'>
                <button className='logout-btn' type='button' onClick={logout}>
                    Logout
                </button>
            </div>
            {/* TODO: Display this in a modal component instead of rendering here */}
            {successMsg && <p>{successMsg}</p>}
            {errorMsg && <p>{errorMsg}</p>}
        </>
    )
}

export default ProfileCard
