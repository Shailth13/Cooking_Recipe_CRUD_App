import React, { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../auth'
import Recipe from '../components/RecipeCard'
import { Modal, Form, Button } from 'react-bootstrap'
import { useForm } from 'react-hook-form'

const LoggedinHome = () => {
  const [recipeList, setRecipes] = useState([])
  const [show, setShow] = useState(false)
  const {
    register,
    handleSubmit,
    setValue,
    formState: { errors },
  } = useForm()
  const [recipeId, setRecipeId] = useState(0)
  const nav = useNavigate()

  useEffect(() => {
    fetch('/recipe/recipes')
      .then((res) => res.json())
      .then((data) => {
        // debugger
        // console.log(data)
        setRecipes(data)
      })
      .catch((err) => console.log(err))
  }, [])

  const getAllRecipes = () => {
    fetch('/recipe/recipes')
      .then((res) => res.json())
      .then((data) => {
        // debugger
        setRecipes(data)
      })
      .catch((err) => console.log(err))
  }

  const closeModal = () => {
    setShow(false)
  }

  const showModal = (id) => {
    setShow(true)
    setRecipeId(id)
    recipeList.map((recipe) => {
      if (recipe.id === id) {
        setValue('name', recipe.name)
        setValue('ingredients', recipe.ingredients)
        setValue('instructions', recipe.instructions)
        setValue('category', recipe.category)
        setValue('serving_size', recipe.serving_size)
        setValue('notes', recipe.notes)
        setValue('date_added', recipe.date_added)
        setValue('date_modified', recipe.date_modified)
      }
    })
  }

  let token = localStorage.getItem('REACT_TOKEN_AUTH_KEY')

  const updateRecipe = (data) => {
    // console.log(data)

    const requestOptions = {
      method: 'PUT',
      headers: {
        'content-type': 'application/json',
        Authorization: `Bearer ${JSON.parse(token)}`,
      },
      body: JSON.stringify(data),
    }

    fetch(`/recipe/recipe/${recipeId}`, requestOptions)
      .then((res) => res.json())
      .then((data) => {
        console.log(data)

        const reload = window.location.reload()
        reload()
      })
      .catch((err) => console.log(err))
  }

  const deleteRecipe = (id) => {
    // console.log(id)

    const requestOptions = {
      method: 'DELETE',
      headers: {
        'content-type': 'application/json',
        Authorization: `Bearer ${JSON.parse(token)}`,
      },
    }

    fetch(`/recipe/recipe/${id}`, requestOptions)
      .then((res) => res.json())
      .then((data) => {
        // console.log(data)
        getAllRecipes()
      })
      .catch((err) => {
        console.log(err)
        alert(err)
      })
  }

  return (
    <div className='recipes container'>
      <Modal show={show} size='lg' onHide={closeModal}>
        <Modal.Header closeButton>
          <Modal.Title>Update Recipe</Modal.Title>
        </Modal.Header>
        <Modal.Body>
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
              <Button variant='primary' onClick={handleSubmit(updateRecipe)}>
                Save
              </Button>
            </Form.Group>
          </form>
        </Modal.Body>
      </Modal>
      <h1>List of Recipes</h1>
      {recipeList && recipeList.length > 0 ? (
        recipeList.map((recipe, index) => (
          <Recipe
            recipeData={recipe}
            key={index}
            onClick={() => {
              showModal(recipe.id)
            }}
            onDelete={() => {
              deleteRecipe(recipe.id)
            }}
          />
        ))
      ) : (
        <>
          <div className='nodata'>
            No Recipes Avaialble, begin by
            <Link to='/create_recipe'> adding some of your favourite recepies</Link>
          </div>
        </>
      )}
    </div>
  )
}

const LoggedOutHome = () => {
  return (
    <div className='home container'>
      <h1 className='heading'>Welcome to the Recipes</h1>
      <Link to='/signup' className='btn btn-primary btn-lg'>
        Get Started
      </Link>
    </div>
  )
}

const HomePage = () => {
  //   debugger
  const [logged] = useAuth()
  //   console.log('status', logged)
  return <div>{logged ? <LoggedinHome /> : <LoggedOutHome />}</div>
}

export default HomePage
