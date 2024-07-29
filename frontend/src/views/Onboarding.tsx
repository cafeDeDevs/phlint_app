import React, { useState } from 'react'
import { z } from 'zod'
import { useNavigate } from 'react-router-dom'

const passwordSchemaRegex = new RegExp(
    [
        /^(?=.*[a-z])/, // At least one lowercase letter
        /(?=.*[A-Z])/, // At least one uppercase letter
        /(?=.*\d)/, // At least one digit
        /(?=.*[!@#$%^&*()_+\-=[\]{};':"\\|,.<>/?])/, // At least one special character
        /[A-Za-z\d!@#$%^&*()_+\-=[\]{};':"\\|,.<>/?]{10,}$/, // At least 10 characters long
    ]
        .map((r) => r.source)
        .join(''),
)

const passwordSchema = z
    .string()
    .regex(
        passwordSchemaRegex,
        'Password must be at least 10 characters long and contain at least one lowercase letter, one uppercase letter, one digit, and one special character.',
    )

const usernameSchema = z
    .string()
    .min(5, 'Username must be at least 5 characters long.')

const Onboarding = () => {
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const [confirmPassword, setConfirmPassword] = useState('')
    const [error, setError] = useState('')
    const navigate = useNavigate()

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setError('')

        try {
            usernameSchema.parse(username)
        } catch (err) {
            if (err instanceof z.ZodError) {
                setError(err.errors[0].message)
            } else {
                setError('An unexpected error occurred.')
            }
            return
        }

        try {
            passwordSchema.parse(password)
        } catch (err) {
            if (err instanceof z.ZodError) {
                setError(err.errors[0].message)
            } else {
                setError('An unexpected error occurred.')
            }
            return
        }

        if (password !== confirmPassword) {
            setError('Passwords do not match')
            return
        }

        const token = new URLSearchParams(window.location.search).get('token')

        try {
            //! Fetch to activate
            const res = await fetch('/api/activate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password, token }),
            })

            if (!res.ok) {
                // Catch server-side error
                const errData = await res.json()
                throw new Error(errData.message || 'Server error')
            }

            //! Redirect to next page
            navigate('/')
        } catch (err: any) {
            // Catch client-side or network error
            console.error(
                'Client error: ',
                err.message || 'Unknown client error',
            )
            setError(
                'A network error occurred. Please check your connection and try again.',
            )
        }
    }

    return (
        <div>
            <h2>Complete Your Registration</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Username:</label>
                    <input
                        type='text'
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label>Password:</label>
                    <input
                        type='password'
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label>Confirm Password:</label>
                    <input
                        type='password'
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
                        required
                    />
                </div>
                {error && <p style={{ color: 'red' }}>{error}</p>}
                <button type='submit'>Complete Registration</button>
            </form>
        </div>
    )
}

export default Onboarding
