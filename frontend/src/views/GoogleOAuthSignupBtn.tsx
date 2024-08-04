import { useGoogleLogin } from '@react-oauth/google'
import { useNavigate } from 'react-router-dom'
import { useState } from 'react'

import { delay } from '../utils/'
import urls from '../config/urls'

// TODO: Add An Onboarding Process that asks the user to create a user_name and other info
const GoogleOAuthSignupBtn = () => {
    const navigate = useNavigate()
    const [errorMsg, setErrorMsg] = useState<string | null>(null)

    const signup = useGoogleLogin({
        onSuccess: async (tokenResponse): Promise<void> => {
            try {
                const res = await fetch(urls.BACKEND_REGISTRATION_ROUTE, {
                    method: 'POST',
                    headers: {
                        Accept: 'application/json',
                        'Content-Type': 'application/json',
                    },
                    credentials: 'include',
                    body: JSON.stringify({
                        code: tokenResponse.code,
                    }),
                })
                if (!res.ok) throw new Error('Error While Authenticating User!')
                navigate('/auth')
            } catch (err) {
                if (err instanceof Error) {
                    console.error('ERROR :=>', err)
                    setErrorMsg(err.message)
                    await delay(3000)
                    navigate('/')
                }
            }
        },
        onError: async (err) => {
            if (err instanceof Error) {
                console.error('ERROR :=>', err.message)
                setErrorMsg(err.message)
                await delay(3000)
                navigate('/')
            }
        },
        flow: 'auth-code',
    })

    return (
        <>
            <button type='button' onClick={() => signup()}>
                Sign Up With Google
            </button>
            {errorMsg && <p>{errorMsg}</p>}
        </>
    )
}

export default GoogleOAuthSignupBtn
