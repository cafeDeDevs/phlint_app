import React, { useState } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { z } from 'zod'

import { delay, usernameSchema, passwordSchema } from '../utils/'
import urls from '../config/urls'

const Onboarding = () => {
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const [confirmPassword, setConfirmPassword] = useState('')
    const [error, setError] = useState('')
    const [success, setSuccess] = useState('')

    const location = useLocation()
    const navigate = useNavigate()

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
                throw new Error(err.errors[0].message)
            } else {
                const error = err as Error
                setError(error.message)
                throw new Error(error.message)
            }
        }

        if (password !== confirmPassword) {
            setError('Passwords do not match')
            throw new Error('Passwords do not match')
        }

        try {
            const res = await fetch(urls.BACKEND_ONBOARD_ROUTE, {
                method: 'POST',
                headers: {
                    Accept: 'application/json',
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({ username, password, token }),
            })

            const jsonRes = await res.json()
            if (!res.ok) {
                throw new Error(jsonRes.message || 'Server error')
            }
            setSuccess(jsonRes.message)
            await delay(3000)
            navigate('/gallery')
        } catch (err) {
            const error = err as Error
            setError(error.message)
            throw new Error(error.message || 'Unknown error')
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
