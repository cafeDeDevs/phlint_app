import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'

const Onboarding = () => {
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const [confirmPassword, setConfirmPassword] = useState('')
    const [error, setError] = useState('')
    const navigate = useNavigate()

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        if (password !== confirmPassword) {
            setError('Passwords do not match!')
            return
        }

        const token = new URLSearchParams(location.search).get('token')

        try {
            const res = await fetch('/api/onboarding-view', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password, token }),
            })

            if (!res.ok) {
                // catch server side error
                const errData = await res.json()
                throw new Error(errData.message)
            }

            // # TODO: navigate elsewhere
            navigate('/')
        } catch (err: any) {
            // cathc either error
            setError('An error occurred: ' + err.message)
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
