import React, { useEffect, useState } from 'react';
import {Chessboard} from "react-chessboard"; // react-chessboard component
import {Chess} from "chess.js";  // chess.js library to provide logic to react-chessboard
import { DataGrid, GridColDef } from '@mui/x-data-grid';


// https://mui.com/x/api/data-grid/grid-col-def/
// Definitions of columns for Material-UI data grid
const columns: GridColDef[] = [
  { field: 'Next Move', 
    headerName: 'Next Move', 
    width: 130,
    sortable: false 
  },
  { field: 'Number of games', 
    headerName: '# of Games',  
    width: 130,
    sortable: false 
  },
  { field: 'Winrate', 
    headerName: 'Winrate', 
    width: 260,
    sortable: false,
    // Display filled winrate percentage  renderCell: (params) => 
  },
];


export default function QueryOpenings() {
  console.log("in app");
  const [game, setGame] = useState(new Chess());  // Creates new chess.js game instance, providing chess rules/logic to react-chessboard
  const [fen, setFen] = useState(game.fen());  // FEN represents a chessboard position, used to update react-chessboard
  // const [rows, setRows] = useState([]);  // To store and update data for the data grid
  // const [currentMoveIndex, setCurrentMoveIndex] = useState(0);  // To keep track of the current move index


  // Sends the player's move to the server for processing
  const sendMoveToServer = async (sourceSq, targetSq, piece) => {

    console.log("in sendMoveToServer")
    console.log(sourceSq, targetSq, piece);

    try {
      const response = await fetch('http://localhost:5000/api/query-openings', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        // Note: The server will need to parse/reformat this JSON data
        body: JSON.stringify({ sourceSq, targetSq, piece})  
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json(); 
      // {Use the response data from the server HERE, e.g. update data grid showing subsequent move frequency}
      // Use setRows() to update data grid
      console.log("Data from server: ", data);
    } 
    
    catch (error) {
      console.error("Failed to send move to server:", error);
    }
  };


  // Handles chess moves on react-chessboard
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

    // Otherwise update chess.js game, FEN for react-chessboard, and send move to server
    const result = game.move({ from: sourceSq, to: targetSq });
    console.log("result before " + result.before + "after" + result.after + " in onDrop");

    setFen(game.fen());
    console.log("Valid move in onDrop");

    sendMoveToServer(sourceSq, targetSq, piece);
    console.log("Move sent to server");

    return true;
  };


  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'start', gap: '24px' }}>
      <div style={{width: "40vw"}}>
        <Chessboard
            position={fen}
            onPieceDrop={onDrop}
        />
      </div>
      <div style={{ height: 400, width: '50vw' }}>
        <DataGrid
          // rows={}
          columns={columns} 
          autoPageSize
          disableRowSelectionOnClick
          disableColumnMenu
          disableColumnResize
          hideFooter
        />
      </div>
    </div>
  );
}