import React, { useState } from 'react';
import './CustomTooltip.css'; // Import the CSS for styling

const CustomTooltip = ({ children, content }) => {
  const [visible, setVisible] = useState(false);

  return (
    <div 
      className="tooltip-container" 
      onMouseEnter={() => setVisible(true)} 
      onMouseLeave={() => setVisible(false)}
    >
      {children}
      {visible && (
        <div className="tooltip-box">
          {content}
        </div>
      )}
    </div>
  );
};

export default CustomTooltip;
