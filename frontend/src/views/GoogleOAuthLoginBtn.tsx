import { useGoogleLogin } from '@react-oauth/google'
import { useNavigate } from 'react-router-dom'
import { useState } from 'react'

const delay = (ms: number): Promise<void> => {
    return new Promise((resolve) => setTimeout(resolve, ms))
}

// TODO: Display Error Messages (especially on 401 Unauthorized Response ,user unauthorized)
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
                    const errorData = await res.json()
                    setErrorMsg(
                        errorData.msg ||
                            'Error while trying to authenticate user. Please sign up.',
                    )
                    await delay(3000)
                    navigate('/signup')
                } else {
                    navigate('/auth')
                }
            } catch (err) {
                console.error('ERROR :=>', err)
                setErrorMsg('An unexpected error occurred. Please try again.')
                await delay(3000)
                navigate('/signup')
            }
        },
        onError: (err) => {
            console.error('ERROR :=>', err)
            setErrorMsg('Login failed. Please sign up.')
            delay(3000).then(() => navigate('/signup'))
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
