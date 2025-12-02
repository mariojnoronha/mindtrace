import { Route,Routes } from 'react-router'
import Landing from './pages/Landing'

const App = () => {
  return (
    <>
      <Routes>
        <Route path='/' element={<Landing />} />
      </Routes>
    </>
  )
}

export default App
