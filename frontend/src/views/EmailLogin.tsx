import React, { useState, type FormEvent } from 'react'
import urls from '../config/urls'
import { z } from 'zod'

// Email validation schema with Zod
const emailSchema = z.object({
    email: z.string().email('Invalid email address'),
})

const EmailLogin: React.FC = () => {
    const [email, setEmail] = useState<string>('')
    const [password, setPassword] = useState<string>('')
    const [message, setMessage] = useState<string>('')

    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault()

        // Validate email with Zod
        const validationRes = emailSchema.safeParse({ email })

        if (!validationRes.success) {
            setMessage(validationRes.error.errors[0].message)
            return
        }

        try {
            // TODO: Create route on BE
            const res = await fetch(urls.BACKEND_EMAIL_LOGIN_ROUTE, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password }),
            })

            if (!res.ok) {
                const jsonRes = await res.json()
                throw new Error(jsonRes.message)
            } else {
                const jsonRes = await res.json()
                setMessage(jsonRes.message)
            }
        } catch (err) {
            const error = err as Error
            console.error('Error: ', error.message)
            setMessage(error.message)
        }
    }

    return (
        <div>
            <h1>Email Login</h1>
            <form onSubmit={handleSubmit}>
                <label htmlFor='email-form'>Email:</label>
                <br />
                <input
                    type='email'
                    id='email-form'
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />
                <br />
                <label htmlFor='password-form'>Password:</label>
                <br />
                <input
                    type='password'
                    id='password-form'
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />
                <br />
                <button type='submit'>Login</button>
            </form>
            {message && <p>{message}</p>}
        </div>
    )
}

export default EmailLogin
