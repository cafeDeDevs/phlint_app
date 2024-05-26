import './App.css'
import { useNavigate } from 'react-router-dom'
/* TODO: Add a prop to be "bubbled up from this component
 * to set a isAuthenticated state, render either this or
 * something different depending on this state" */
/* TODO: Also Setup signup logic on both front end and backend */

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
