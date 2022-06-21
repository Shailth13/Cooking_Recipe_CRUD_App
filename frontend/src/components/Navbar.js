import React from 'react'
import { Link } from 'react-router-dom'
import { useAuth, logout } from '../auth'
import './components.css'

// the Sign In navigation component

const SignInRoutes = () => {
  return (
    <>
      <li className='nav-item'>
        <Link className='nav-link active' to='/'>
          Home
        </Link>
      </li>
      <li className='nav-item'>
        <Link className='nav-link  active' to='/create_recipe'>
          Create Recipes
        </Link>
      </li>
      <li className='nav-item'>
        <div
          className='nav-link active logout'
          onClick={() => {
            logout()
          }}
        >
          Log Out
        </div>
      </li>
    </>
  )
}

// the Sign Out/Sign UP Default navigation component

const SignOutRoutes = () => {
  return (
    <>
      <li className='nav-item'>
        <Link className='nav-link active' to='/'>
          Home
        </Link>
      </li>
      <li className='nav-item'>
        <Link className='nav-link active' to='/signup'>
          Sign Up
        </Link>
      </li>
      <li className='nav-item'>
        <Link className='nav-link active' to='/signin'>
          Sign In
        </Link>
      </li>
    </>
  )
}

// The navbar for implementing navigation switching between SignIn and SignUp default component.

const NavBar = () => {
  const [logged] = useAuth()

  return (
    <nav className='navbar navbar-expand-lg navbar-dark bg-dark'>
      <div className='container-fluid'>
        <Link className='navbar-brand' to='/'>
          Cook Book
        </Link>
        <button
          className='navbar-toggler'
          type='button'
          data-bs-toggle='collapse'
          data-bs-target='#navbarNav'
          aria-controls='navbarNav'
          aria-expanded='false'
          aria-label='Toggle navigation'
        >
          <span className='navbar-toggler-icon'></span>
        </button>
        <div className='collapse navbar-collapse' id='navbarNav'>
          <ul className='navbar-nav'>{logged ? <SignInRoutes /> : <SignOutRoutes />}</ul>
        </div>
      </div>
    </nav>
  )
}

export default NavBar
