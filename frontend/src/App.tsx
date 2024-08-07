import './App.css'
import { useNavigate } from 'react-router-dom'

const App = () => {
    const navigate = useNavigate()
    const goToSignup = () => navigate('/signup')
    const goToLogin = () => navigate('/login')

    return (
        <>
            <div className='splash-page'>
                <h1>App Home Splash Page</h1>
                <button onClick={() => goToSignup()}>Sign Up</button>
                <br />
                <button onClick={() => goToLogin()}>Login</button>
            </div>
        </>
    )
}

export default App
