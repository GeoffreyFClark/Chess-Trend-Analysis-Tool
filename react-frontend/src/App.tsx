import { useState, useEffect } from 'react'
import { Routes, Route, Link } from 'react-router-dom';
import './App.css';
import QueryOpenings from './query_openings';
import QueryResults from './query_results';
import TestQuery from './test-query';
import Navigation from './navigation';
import Home from './home';
import Login from './Login';
import Register from './Register';


function App() {

  return (
    <div>
      <nav>
        <Navigation />
      </nav>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/query-openings" element={<QueryOpenings />} />
        <Route path="/query-results" element={<QueryResults />} />
        <Route path="/test-query" element={<TestQuery />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
      </Routes>
    </div>
  );
}

export default App