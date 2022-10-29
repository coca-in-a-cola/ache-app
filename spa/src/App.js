import React from 'react';
import './index.css';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  useLocation,
  useParams,
  useNavigate,
} from 'react-router-dom';

import { News } from './components/Pages/News'
import { Main } from './components/Pages/Main'
import { Papers } from './components/Pages/Papers'

const FuckYouReactRouterV6 = (props) => {
    const params = useParams()

    const nextProps = {... props, ...props.mapParamsToProps?.(params)}
    const location = useLocation()
    const navigate = useNavigate()
    console.log(location)
    return (
      <props.element location={location.pathname} navigate={navigate} {... nextProps} />
    )
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/maps/:category" element={
          <FuckYouReactRouterV6 
          mapParamsToProps={params => {
            return {entity: "/api/maps/" + params.category}
          }} 
          element={News}
          />
        } />
        <Route path="/news" element={<FuckYouReactRouterV6 element={News} entity={"/api/news"} /> }/>
        <Route path="/papers" element={<FuckYouReactRouterV6 element={Papers} />} />
        <Route path="/forms/:uuid" element={
          <FuckYouReactRouterV6 
          mapParamsToProps={params => {
            return {form_uuid: params.uuid}
          }}
          location={"/"}
          element={Main}
          />
        } />
        <Route path="*" element={<FuckYouReactRouterV6 element={Main} />} />
      </Routes>
    </Router>
  );
}

export default App;
