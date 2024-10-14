import React from 'react';

const Navbar: React.FC = () => {
  return (
    <nav className="bg-stone-600 p-4 text-white rounded-sm shadow-md">
      <div className="container mx-auto flex justify-between items-center">
        <a href="/" className="text-2xl font-bold">
          Permit ReBAC Visualizer
        </a>
        <div className="space-x-4">
          <a
            href="https://www.permit.io/"
            rel="noreferrer"
            target="_blank"
            className="hover:text-blue-200">
            Learn More
          </a>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
