import React, { useState } from 'react'
import { useLocation } from 'react-router-dom'
import { z } from 'zod'

import { usernameSchema, passwordSchema } from '../utils/'

const Onboarding = () => {
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const [confirmPassword, setConfirmPassword] = useState('')
    const [error, setError] = useState('')
    const [success, setSuccess] = useState('')

    const location = useLocation()

    const queryParams = new URLSearchParams(location.search)
    const token = queryParams.get('token')

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setError('')
        setSuccess('')

        try {
            usernameSchema.parse(username)
        } catch (err) {
            if (err instanceof z.ZodError) {
                setError(err.errors[0].message)
                throw new Error(err.errors[0].message)
            } else {
                const error = err as Error
                setError(error.message)
                throw new Error(error.message)
            }
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

        try {
            const res = await fetch(
                import.meta.env.VITE_BACKEND_ONBOARD_ROUTE,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ username, password, token }),
                },
            )

            const jsonRes = await res.json()
            if (!res.ok) {
                throw new Error(jsonRes.message || 'Server error')
            }
            setSuccess(jsonRes.message)
        } catch (err) {
            const error = err as Error
            console.error(error.message || 'Unknown error')
            setError(error.message)
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
                {success && <p style={{ color: 'green' }}>{success}</p>}
                <button type='submit'>Complete Registration</button>
            </form>
        </div>
    )
}

export default Onboarding
