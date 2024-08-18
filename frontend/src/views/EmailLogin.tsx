import React, { useState, type FormEvent } from 'react'

// TODO: Add An Onboarding Process that asks the user to create a user_name and other info
const EmailLogin: React.FC = () => {
    const [email, setEmail] = useState<string>('')
    const [password, setPassword] = useState<string>('')

    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault()
        console.log('Submitted email: ', email)
        console.log('Submitted password: ', password)
    }

    return (
        <>
            <div
                style={{
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    justifyContent: 'center',
                    height: '100vh',
                }}>
                <h1>Login With Email!</h1>
                <form
                    onSubmit={handleSubmit}
                    style={{
                        display: 'flex',
                        flexDirection: 'column',
                        width: '300px',
                    }}>
                    <input
                        type='email'
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder='Enter your email'
                        required
                    />
                    <input
                        type='password'
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder='Enter your password'
                        required
                    />
                    <button type='submit'>Submit</button>
                </form>
            </div>
        </>
    )
}

export default EmailLogin
