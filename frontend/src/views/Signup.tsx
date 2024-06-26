import { GoogleOAuthProvider } from '@react-oauth/google'
import GoogleOAuthSignupBtn from './GoogleOAuthSignupBtn'
const googleClientId = import.meta.env.VITE_GOOGLE_OAUTH2_CLIENT_ID

// TODO: Set up where if the User is
// already logged in they are taken to AuthPage
const Signup = () => {
    return (
        <>
            <GoogleOAuthProvider clientId={googleClientId}>
                <GoogleOAuthSignupBtn />
            </GoogleOAuthProvider>
        </>
    )
}

export default Signup
