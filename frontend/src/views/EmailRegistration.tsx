import { type FC, useState, FormEvent } from 'react'

const EmailRegistrationForm: FC = () => {
    const [email, setEmail] = useState<string>('')
    const [message, setMessage] = useState<string>('')

    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault()
        try {
            const res = await fetch(
                import.meta.env.VITE_BACKEND_EMAIL_REGISTRATION_ROUTE,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ email }),
                },
            )
            // TODO: Remove else clause and simply navigate('/onboarding')
            // NOTE: onboarding route not yet implemented
            if (!res.ok) {
                const jsonRes = await res.json()
                throw new Error(jsonRes.message)
            } else {
                const jsonRes = await res.json()
                setMessage(jsonRes.message)
            }
        } catch (err) {
            const error = err as Error
            console.error('ERROR :=>', error.message)
            setMessage(error.message)
        }
    }

    return (
        <div>
            <h1>Email Registration</h1>
            <form onSubmit={handleSubmit}>
                <label htmlFor='email-form'>Please Enter Your Email:</label>
                <br />
                <input
                    type='email'
                    id='email-form'
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />
                <br />
                <button type='submit'>Register</button>
            </form>
            {message && <p>{message}</p>}
        </div>
    )
}

export default EmailRegistrationForm
