import React, { useEffect, useState } from 'react'
import ReactDOM from 'react-dom'
import axios from 'axios'

const App = () => {
  const [message, setMessage] = useState('')

  useEffect(() => {
    axios
      .request('/recipe/fetch')
      .then((response) => {
        console.log(response.data)
        setMessage(response.data.message)
      })
      .catch((err) => {
        console.log('error: ' + err)
      })
  }, [])
  return <div className='app'>{message}</div>
}

ReactDOM.render(<App />, document.getElementById('root'))
