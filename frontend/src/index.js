import 'bootstrap/dist/css/bootstrap.min.css'
import './styles/index.css'
import React from 'react'
import ReactDOM from 'react-dom'
import NavBar from './components/Navbar'

import { BrowserRouter, Route, Routes } from 'react-router-dom'
import HomePage from './components/Home'
import SignUpPage from './components/SignUp'
import SignInPage from './components/SignIn'
import CreateRecipePage from './components/CreateRecipe'
import NoMatch from './components/NoMatch'

const App = () => {
  return (
    <BrowserRouter>
      <NavBar />
      <Routes>
        <Route path='/create_recipe' element={<CreateRecipePage />} />
        <Route path='/signin' element={<SignInPage />} />
        <Route path='/signup' element={<SignUpPage />} />
        <Route path='/' element={<HomePage />} />
        <Route path='*' element={<NoMatch />} />
      </Routes>
    </BrowserRouter>
  )
}

ReactDOM.render(<App />, document.getElementById('root'))
