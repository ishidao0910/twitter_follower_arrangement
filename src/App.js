import React from "react";

const App = () => {
  const onClickButton = () => alert();
  const contentStyle = {
    color: 'blue',
    fontSize: '18px'
  }
  return (
    <React.Fragment>
      <h1 style={{ color: 'red' }}> test h1 </h1>
      <p style={contentStyle}> test p tag </p>
      <button onClick={onClickButton}> ボタン </button>
    </React.Fragment>
  );
};

export default App;
