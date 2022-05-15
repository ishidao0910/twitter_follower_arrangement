import React, { useEffect, useState } from "react";
import ColorfulMessage from "./conponents/ColorfulMessage";

const App = () => {
  const [num, setNum] = useState(0);
  const [faceShowFlag, setFaceShowFlag] = useState(false);

  const onClickCountUp = () => {
    setNum(num + 1);
  };

  const onClickSwitchShowFlag = () => {
    setFaceShowFlag(!faceShowFlag);
  };

  useEffect(() => {
    if (num > 0) {
      if (num % 3 === 0) {
        faceShowFlag || setFaceShowFlag(true);
      } else {
        faceShowFlag && setFaceShowFlag(false);
      }
    }
  }, [num, faceShowFlag]);

  return (
    <React.Fragment>
      <h1 style={{ color: "red" }}> test h1 </h1>
      <ColorfulMessage color="blue"> お元気ですか </ColorfulMessage>
      <ColorfulMessage color="pink"> 元気です </ColorfulMessage>
      <button onClick={onClickCountUp}> カウントアップ </button>
      <br />
      <button onClick={onClickSwitchShowFlag}> on/off </button>
      <p> {num} </p>
      {faceShowFlag && <p>( '_')</p>}
    </React.Fragment>
  );
};

export default App;
