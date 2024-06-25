//! The primary issue with the GoogleOAuthLoginBtn component as it
//! stands is that it does not store the access_token and refresh_token in localStorage after a successful
//! login. To store these tokens, we need to ensure that the response from the backend (after a successful login) contains these tokens and they are properly saved to localStorage.

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
                }

                const jsonRes = await res.json()

                console.log('Login successful, storing tokens: ', jsonRes)

                localStorage.setItem('access_token', jsonRes.access_token)
                localStorage.setItem('refresh_token', jsonRes.refresh_token)
                console.log('Stored access token:', jsonRes.access_token)
                console.log('Stored refresh token:', jsonRes.refresh_token)

                navigate('/auth')
            } catch (err) {
                if (err instanceof Error) {
                    console.error('ERROR :=>', err.message)
                    setErrorMsg(err.message)
                    await delay(3000)
                    navigate('/signup')
                }
            }
        },
        onError: async (err) => {
            if (err instanceof Error) {
                console.error('ERROR :=>', err.message)
                setErrorMsg(err.message)
                await delay(3000)
                navigate('/signup')
            }
        },
        flow: 'auth-code',
    })

    return (
        <div>
            <button type='button' onClick={() => login()}>
                Login With Google
            </button>
            {errorMsg && <p>{errorMsg}</p>}
        </div>
    )
}

export default GoogleOAuthLoginBtn

// import { useGoogleLogin } from '@react-oauth/google'
// import { useNavigate } from 'react-router-dom'
// import { useState } from 'react'

// import { delay } from '../utils/'

// const GoogleOAuthLoginBtn = () => {
//     const navigate = useNavigate()
//     const [errorMsg, setErrorMsg] = useState<string | null>(null)

//     const login = useGoogleLogin({
//         onSuccess: async (tokenResponse): Promise<void> => {
//             try {
//                 const res = await fetch(
//                     import.meta.env.VITE_BACKEND_LOGIN_ROUTE,
//                     {
//                         method: 'POST',
//                         headers: {
//                             Accept: 'application/json',
//                             'Content-Type': 'application/json',
//                         },
//                         credentials: 'include',
//                         body: JSON.stringify({
//                             code: tokenResponse.code,
//                         }),
//                     },
//                 )

//                 if (!res.ok) {
//                     const jsonRes = await res.json()
//                     throw new Error(jsonRes.message)
//                 }
//                 navigate('/auth')
//             } catch (err) {
//                 if (err instanceof Error) {
//                     console.error('ERROR :=>', err.message)
//                     setErrorMsg(err.message)
//                     await delay(3000)
//                     navigate('/signup')
//                 }
//             }
//         },
//         onError: async (err) => {
//             if (err instanceof Error) {
//                 console.error('ERROR :=>', err.message)
//                 setErrorMsg(err.message)
//                 await delay(3000)
//                 navigate('/signup')
//             }
//         },
//         flow: 'auth-code',
//     })

//     return (
//         <div>
//             <button type='button' onClick={() => login()}>
//                 Login With Google
//             </button>
//             {errorMsg && <p>{errorMsg}</p>}
//         </div>
//     )
// }

// export default GoogleOAuthLoginBtn
