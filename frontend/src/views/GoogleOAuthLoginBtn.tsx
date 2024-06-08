import { useGoogleLogin } from '@react-oauth/google'
import { useNavigate } from 'react-router-dom'
import { useState } from 'react'

import { delay } from '../utils/'

const GoogleOAuthLoginBtn = () => {
    const navigate = useNavigate()
    const [errorMsg, setErrorMsg] = useState<string | null>(null)

    const login = useGoogleLogin({
        onSuccess: async (tokenResponse): Promise<void> => {
            try {
                const res = await fetch(
                    import.meta.env.VITE_BACKEND_LOGIN_ROUTE,
                    {
                        method: 'POST',
                        headers: {
                            Accept: 'application/json',
                            'Content-Type': 'application/json',
                        },
                        credentials: 'include',
                        body: JSON.stringify({
                            code: tokenResponse.code,
                        }),
                    },
                )

                if (!res.ok) {
                    const jsonRes = await res.json()
                    throw new Error(jsonRes.message)
                } else navigate('/auth')
            } catch (err) {
                if (err instanceof Error) {
                    console.error('ERROR :=>', err.message)
                    setErrorMsg(
                        err.message ||
                            'Error occured while authenticating. Please sign up.',
                    )
                    await delay(3000)
                    navigate('/signup')
                }
            }
        },
        onError: async (err) => {
            if (err instanceof Error) {
                console.error('ERROR :=>', err.message)
                setErrorMsg(
                    err.message ||
                        'Error occured while authenticating. Please sign up.',
                )
                await delay(3000)
                navigate('/signup')
            }
        },
        flow: 'auth-code',
    })

    return (
        <div>
            <button onClick={() => login()}>Login With Google</button>
            {errorMsg && <p>{errorMsg}</p>}
        </div>
    )
}

export default GoogleOAuthLoginBtn
