// Simple header component.
import React from 'react';

const Header = () => (
  <header className="bg-white shadow-sm p-4">
    <div className="flex items-center justify-between px-4 md:px-8 lg:px-16">
      <h1 className="text-2xl font-bold text-gray-900">
        Birhan Energies
      </h1>
      <p className="text-sm text-gray-500 hidden sm:block">
        Brent Oil Change Point Analysis Dashboard
      </p>
    </div>
  </header>
);

export default Header;