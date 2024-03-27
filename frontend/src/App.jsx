import React, { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [data, setData] = useState([])

  // testing react + flask communication
  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    const response = await fetch('http://127.0.0.1:5000/test_data')
    const data = await response.json()
    setData(data)
    console.log(data)
  }

  return (
    <>
    </>
  )
}

export default App
