import React, { useState } from 'react'
import { Form, Button } from 'react-bootstrap'
import { useForm } from 'react-hook-form'
import IconButton from '@mui/material/IconButton'
import './components.css'

const CreateRecipePage = () => {
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm()
  const [show, setShow] = useState(false)

  const createRecipe = (data) => {
    // console.log(data)

    const token = localStorage.getItem('REACT_TOKEN_AUTH_KEY')
    // console.log(token)

    const requestOptions = {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
        Authorization: `Bearer ${JSON.parse(token)}`,
      },
      body: JSON.stringify(data),
    }

    fetch('/recipe/recipes', requestOptions)
      .then((res) => res.json())
      .then((data) => {
        reset()
        alert('recipe created successfully')
      })
      .catch((err) => console.log(err))
  }

  return (
    <div className='container'>
      <h1>Create A Recipe</h1>
      <br></br>
      <form>
        <Form.Group>
          <Form.Label>Recipe Name</Form.Label>
          <Form.Control type='text' {...register('name', { required: true, maxLength: 25 })} />
        </Form.Group>
        {errors.name && (
          <p style={{ color: 'red' }}>
            <small>Name is required</small>
          </p>
        )}
        {errors.name?.type === 'maxLength' && (
          <p style={{ color: 'red' }}>
            <small>Name should be less than 25 characters</small>
          </p>
        )}
        <br></br>
        <Form.Group>
          <Form.Label>Ingredients</Form.Label>
          <Form.Control as='textarea' rows={5} {...register('ingredients', { required: true, maxLength: 255 })} />
        </Form.Group>
        {errors.ingredients && (
          <p style={{ color: 'red' }}>
            <small>Ingredients are required</small>
          </p>
        )}
        {errors.ingredients?.type === 'maxLength' && (
          <p style={{ color: 'red' }}>
            <small>Ingredients description should be less than 255 characters</small>
          </p>
        )}
        <br></br>
        <Form.Group>
          <Form.Label>Instructions</Form.Label>
          <Form.Control as='textarea' rows={5} {...register('instructions', { required: true, maxLength: 1000 })} />
        </Form.Group>
        {errors.instructions && (
          <p style={{ color: 'red' }}>
            <small>instructions are required</small>
          </p>
        )}
        {errors.instructions?.type === 'maxLength' && (
          <p style={{ color: 'red' }}>
            <small>instructions description should be less than 1000 characters</small>
          </p>
        )}
        <br></br>
        <Form.Group>
          <Form.Label>Category</Form.Label>
          <Form.Control as='textarea' rows={5} {...register('category', { required: true, maxLength: 100 })} />
        </Form.Group>
        {errors.category && (
          <p style={{ color: 'red' }}>
            <small>category are required</small>
          </p>
        )}
        {errors.category?.type === 'maxLength' && (
          <p style={{ color: 'red' }}>
            <small>category description should be less than 100 characters</small>
          </p>
        )}
        <br></br>
        <Form.Group>
          <Form.Label>Serving Size</Form.Label>
          <Form.Control as='textarea' rows={5} {...register('serving_size', { required: true, maxLength: 100 })} />
        </Form.Group>
        {errors.serving_size && (
          <p style={{ color: 'red' }}>
            <small>serving_size are required</small>
          </p>
        )}
        {errors.serving_size?.type === 'maxLength' && (
          <p style={{ color: 'red' }}>
            <small>serving_size description should be less than 100 characters</small>
          </p>
        )}
        <br></br>
        <Form.Group>
          <Form.Label>Notes</Form.Label>
          <Form.Control as='textarea' rows={5} {...register('notes', { required: true, maxLength: 1000 })} />
        </Form.Group>
        {errors.notes && (
          <p style={{ color: 'red' }}>
            <small>notes are required</small>
          </p>
        )}
        {errors.notes?.type === 'maxLength' && (
          <p style={{ color: 'red' }}>
            <small>notes description should be less than 1000 characters</small>
          </p>
        )}
        <br></br>
        <Form.Group>
          <IconButton onClick={handleSubmit(createRecipe)}>
            <i className='fa-solid fa-floppy-disk'></i>
          </IconButton>
        </Form.Group>
      </form>
    </div>
  )
}

export default CreateRecipePage
