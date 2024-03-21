import React, { useEffect, useState } from 'react';
import {Chessboard} from "react-chessboard";
import {Chess} from "chess.js";


export default function QueryOpenings() {
  console.log("in app");
  const [game, setGame] = useState(new Chess());
  const [fen, setFen] = useState(game.fen());
  // const [currentMoveIndex, setCurrentMoveIndex] = useState(0);



  const sendMoveToServer = async (sourceSq, targetSq, piece) => {
    console.log("in sendMoveToServer")
    console.log(sourceSq, targetSq, piece);
    try {
      const response = await fetch('http://localhost:5000/api/query-openings', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        // Note: The server will need to parse/reformat this JSON data in body
        body: JSON.stringify({ sourceSq, targetSq, piece})  
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // {Use the response data from the server here, e.g. update table showing subsequent move frequency}

      console.log(data);
    } catch (error) {
      console.error("Failed to send move to server:", error);
    }
  };

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

    const result = game.move({ from: sourceSq, to: targetSq });
    console.log("result before " + result.before + "after" + result.after + " in onDrop");

    setFen(game.fen());
    console.log("Valid move in onDrop");

    sendMoveToServer(sourceSq, targetSq, piece);
    console.log("Move sent to server");

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