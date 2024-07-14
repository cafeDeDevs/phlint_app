import { GoogleOAuthProvider } from '@react-oauth/google'
import GoogleOAuthLoginBtn from './GoogleOAuthLoginBtn'
const googleClientId = import.meta.env.VITE_GOOGLE_OAUTH2_CLIENT_ID

const Login = () => {
    return (
        <>
            <div className='login-card'>
                <GoogleOAuthProvider clientId={googleClientId}>
                    <GoogleOAuthLoginBtn />
                </GoogleOAuthProvider>
            </div>
        </>
    )
}

export default Login
