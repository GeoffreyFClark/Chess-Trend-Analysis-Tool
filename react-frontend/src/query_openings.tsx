import React, { useEffect, useState } from 'react';
import {Chessboard} from "react-chessboard";
import {Chess} from "chess.js";


export default function QueryOpenings() {
  console.log("in app");
  const [game, setGame] = useState(new Chess());
  const [fen, setFen] = useState(game.fen());
  const [currentMoveIndex, setCurrentMoveIndex] = useState(0);

  

  const onDrop = (sourceSq, targetSq, piece) => {
    console.log(sourceSq);
    console.log(targetSq);
    console.log(piece);

    // Check if the move is legal using chess.js
    const legalMoves = game.moves({ square: sourceSq, verbose: true });
    const isValidMove = legalMoves.some(legalMove => legalMove.to === targetSq);

    if (!isValidMove) {
      return false; // Exit if the move isn't legal
    }

    // Make the move on chess.js
    const result = game.move({ from: sourceSq, to: targetSq });
    console.log("result before " + result.before + "after" + result.after + " in onDrop");

    setFen(game.fen());
    console.log("Valid move in onDrop");
    return true;
  };

  return (
    <div style={{width: "50vw"}}>
      <Chessboard
          position={fen}
          onPieceDrop={onDrop}
      />
    </div>
  );
}