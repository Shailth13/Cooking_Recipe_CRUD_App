import React from 'react'

const NoMatch = () => {
  return (
    <div
      className='error'
      style={{
        width: '100%',
        background: 'red',
        padding: '5px',
        display: 'inline-block',
        color: '#fff',
        textAlign: 'center',
        margin: '0.5rem',
      }}
    >
      Path not avaialble, please use navigation bar instaed of writing direct routes in the url!
    </div>
  )
}

export default NoMatch
