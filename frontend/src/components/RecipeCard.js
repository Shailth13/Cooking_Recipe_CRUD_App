import React from 'react'
import { Card } from 'react-bootstrap'
import './components.css'
import { format } from 'date-fns'
import IconButton from '@mui/material/IconButton'

const Recipe = ({ recipeData, onClick, onDelete }) => {
  const { name, ingredients, instructions, category, serving_size, notes, date_added, date_modified } = recipeData
  debugger

  return (
    <Card className='recipe'>
      <Card.Body>
        <Card.Title>Name: {name}</Card.Title>
        <div>Ingredients: {ingredients}</div>
        <div>
          <h4>Preperation Method :</h4> {instructions}
        </div>
        <div>
          <h4>Category :</h4> {category}
        </div>
        <div>
          <h4>Serving Size :</h4>
          {serving_size}
        </div>
        <div>
          <h4>Notes :</h4> {notes}
        </div>
        <div>
          <span>Date Added : {date_added}</span>
        </div>
        <div>
          <span>Updates : {date_modified}</span>
        </div>
        <div className='controlElements'>
          <IconButton onClick={onClick}>
            <i className='fa-solid fa-gear'></i>
          </IconButton>

          <IconButton onClick={onDelete}>
            <i className='fa-solid fa-trash-can'></i>
          </IconButton>
        </div>
      </Card.Body>
    </Card>
  )
}

export default Recipe
