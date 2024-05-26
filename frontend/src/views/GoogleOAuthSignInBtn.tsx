import { useGoogleLogin } from '@react-oauth/google'
import { useNavigate } from 'react-router-dom'

const GoogleOAuthSignInBtn = () => {
    const navigate = useNavigate()
    const login = useGoogleLogin({
        onSuccess: async (tokenResponse): Promise<void> => {
            try {
                const res = await fetch(
                    import.meta.env.VITE_BACKEND_REGISTRATION_ROUTE,
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
                if (!res.ok) throw new Error('Error While Authenticating User!')
                navigate('/auth')
            } catch (err) {
                console.error('ERROR :=>', err)
                navigate('/')
            }
        },
        onError: (err) => {
            console.error('ERROR :=>', err)
            navigate('/')
        },
        flow: 'auth-code',
    })

    return <button onClick={() => login()}>Sign In With Google</button>
}

export default GoogleOAuthSignInBtn
