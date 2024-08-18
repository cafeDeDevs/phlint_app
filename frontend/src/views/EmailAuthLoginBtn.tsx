import { useNavigate } from 'react-router-dom'

const EmailAuthLoginBtn = () => {
    // TODO: Frontend Login By Email Logic Goes here
    const navigate = useNavigate()

    const handleClick = () => {
        navigate('/email-login')
    }
    return (
        <>
            <button type='button' onClick={() => handleClick()}>
                Login With Email
            </button>
        </>
    )
}

export default EmailAuthLoginBtn
