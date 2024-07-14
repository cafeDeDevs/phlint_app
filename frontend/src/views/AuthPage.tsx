import { useNavigate } from 'react-router-dom'
import { useEffect } from 'react'

import { delay } from '../utils/'

const AuthPage = () => {
    const navigate = useNavigate()
    useEffect(() => {
        const redirectToGallery = async () => {
            await delay(3000)
            navigate('/gallery')
        }
        redirectToGallery()
    }, [navigate])

    return (
        <>
            <div className='auth-page'>
                <div>Congratulations! You Are Authenticated!</div>
                <div>One Moment While We Redirect You To Your Gallery!...</div>
            </div>
        </>
    )
}

export default AuthPage
