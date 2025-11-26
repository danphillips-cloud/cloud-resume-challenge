import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './assets/stylesheets/style.css'
import App from './App.jsx'

createRoot(document.querySelector('main')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
