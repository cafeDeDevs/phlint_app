import React, { useState, FormEvent } from 'react'

const EmailRegistrationForm: React.FC = () => {
    const [email, setEmail] = useState<string>('')
    const [message, setMessage] = useState<string>('')

    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault()
        try {
            const response = await fetch(
                import.meta.env.VITE_BACKEND_EMAIL_REGISTRATION_ROUTE,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ email }),
                },
            )
            const data = await response.json()
            if (response.ok) {
                setMessage(data.message)
            } else {
                setMessage('Failed to send email. Please try again.')
            }
        } catch (error) {
            console.error('Error:', error)
            setMessage('Failed to send email. Please try again.')
        }
    }

    return (
        <div>
            <h1>Email Registration</h1>
            <form onSubmit={handleSubmit}>
                <label>
                    Email:
                    <input
                        type='email'
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                </label>
                <button type='submit'>Register</button>
            </form>
            {message && <p>{message}</p>}
        </div>
    )
}

export default EmailRegistrationForm
