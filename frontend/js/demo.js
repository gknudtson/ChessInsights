import { Chessground } from '@lichess-org/chessground';
import '@lichess-org/chessground/assets/chessground.base.css';
import '@lichess-org/chessground/assets/chessground.brown.css';
import '@lichess-org/chessground/assets/chessground.cburnett.css';

Chessground(document.getElementById('board-1'), {});
Chessground(document.getElementById('board-2'), {
  fen: 'r2q2k1/1p6/p2p4/2pN1rp1/N1Pb2Q1/8/PP1B4/R6K b - - 2 25',
});
Chessground(document.getElementById('board-3'), {
  drawable: {
    autoShapes: [
      {
        orig: 'a2',
        dest: 'a6',
        brush: 'green',
        label: { text: 'A' },
        modifiers: {
          hilite: '#fff',
        },
      },
      {
        orig: 'b2',
        dest: 'b6',
        brush: 'blue',
        label: { text: 'B' },
        modifiers: {
          lineWidth: 6,
        },
      },
      {
        orig: 'c2',
        dest: 'c4',
        brush: 'red',
        label: { text: 'C' },
      },
      {
        orig: 'd2',
        dest: 'd3',
        brush: 'green',
        label: { text: 'D' },
      },
      {
        orig: 'f1',
        dest: 'h3',
        brush: 'blue',
        label: { text: 'F' },
      },
      {
        orig: 'g1',
        dest: 'f3',
        brush: 'yellow',
        label: { text: 'E' },
      },
    ],
  },
});
Chessground(document.getElementById('board-4'), {
  orientation: 'black',
  coordinatesOnSquares: true,
  ranksPosition: 'left',
});
Chessground(document.getElementById('board-5'), {
  orientation: 'white',
  coordinatesOnSquares: true,
});
