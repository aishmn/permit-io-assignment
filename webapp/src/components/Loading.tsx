import React from 'react';

const Loading: React.FC = () => {
  return (
    <div className="flex space-x-2 justify-center items-center  mt-10">
      <span className="sr-only">Loading...</span>
      <div className="h-8 w-8 bg-stone-500 rounded-full animate-bounce [animation-delay:-0.3s]" />
      <div className="h-8 w-8 bg-stone-700 rounded-full animate-bounce [animation-delay:-0.15s]" />
      <div className="h-8 w-8 bg-stone-900 rounded-full animate-bounce" />
    </div>
  );
};

export default Loading;
