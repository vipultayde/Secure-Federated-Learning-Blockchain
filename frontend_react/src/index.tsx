import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App'

console.log('Main starting');
const root = document.getElementById('root');
if (!root) {
  console.error('Root element not found');
} else {
  console.log('Root element found', root);
  createRoot(root).render(
    <StrictMode>
      <App />
    </StrictMode>,
  )
}
