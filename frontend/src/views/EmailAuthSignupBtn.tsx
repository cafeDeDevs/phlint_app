import { useNavigate } from 'react-router-dom'

// TODO: Add An Onboarding Process that asks the user to create a user_name and other info
const EmailAuthSignupBtn: React.FC = () => {
    const navigate = useNavigate()

    const handleClick = () => {
        navigate('/email-registration')
    }

    return (
        <>
            <button type='button' onClick={handleClick}>
                Signup With Email
            </button>
        </>
    )
}

export default EmailAuthSignupBtn
