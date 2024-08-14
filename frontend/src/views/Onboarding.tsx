import React, { useEffect, useState } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { z } from 'zod'

import { delay, usernameSchema, passwordSchema } from '../utils/'
import urls from '../config/urls'

const Onboarding = () => {
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const [confirmPassword, setConfirmPassword] = useState('')
    const [error, setError] = useState('')
    const [checkHashError, setCheckHashError] = useState('')
    const [success, setSuccess] = useState('')

    const location = useLocation()
    const navigate = useNavigate()

    const queryParams = new URLSearchParams(location.search)
    const token = queryParams.get('token')

    useEffect(() => {
        if (!token) {
            navigate('/')
            return
        }
        (async () => {
            try {
                const res = await fetch(urls.BACKEND_CHECK_TOKEN_ROUTE, {
                    method: 'POST',
                    headers: {
                        Accept: 'application/json',
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ "token": token }),
                })
                const jsonRes = await res.json()
                if (!res.ok) throw new Error(jsonRes.message)
            } catch (err) {
                const error = err as Error
                setCheckHashError(error.message)
                await delay(3000)
                navigate('/')
                throw new Error(error.message)
            }
        })()
    }, [token, navigate])

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
            if (!res.ok) throw new Error(jsonRes.message)
            setSuccess(jsonRes.message)
            await delay(3000)
            navigate('/gallery')
            return
        } catch (err) {
            const error = err as Error
            setError(error.message)
            throw new Error(error.message || 'Unknown error')
        }
    }

    return (
        <>
            {!checkHashError &&
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
                        <button type='submit'>Complete Registration</button>
                    </form>
                </div>
            }
            <div>
                {error && <p style={{ color: 'red' }}>{error}</p>}
                {success && <p style={{ color: 'green' }}>{success}</p>}
            </div>
        </>
    )
}

export default Onboarding
