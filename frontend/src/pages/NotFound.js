import React from 'react';
import { Link } from 'react-router-dom';

const NotFound = () => {
  return (
    <div>
      <h1>Page Not Found</h1>
      <p>Sorry! The page you are looking for does not exist.</p>
      <p>
        <Link to="/">Click here to return to the homepage.</Link>
      </p>
    </div>
  );
};

export default NotFound;
