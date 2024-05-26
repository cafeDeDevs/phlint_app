import './App.css'
import { useNavigate } from 'react-router-dom'

const App = () => {
    const navigate = useNavigate()
    const goToLogin = () => navigate('/login')
    return (
        <>
            <h1>App Home Splash Page</h1>
            <button onClick={() => goToLogin()}>Login</button>
        </>
    )
}

export default App
