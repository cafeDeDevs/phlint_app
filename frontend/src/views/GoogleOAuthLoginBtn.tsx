import { useGoogleLogin } from '@react-oauth/google'
import { useNavigate } from 'react-router-dom'

// TODO: Display Error Messages (especially on 401 Unauthorized Response ,user unauthorized)
const GoogleOAuthLoginBtn = () => {
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

    return <button onClick={() => login()}>Login With Google</button>
}

export default GoogleOAuthLoginBtn
