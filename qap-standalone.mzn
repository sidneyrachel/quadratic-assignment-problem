include "alldifferent.mzn";

int: n = 12;
array [1..n] of var 1..n: assigned_facilities;
set of int: indices = 1..n;
array [indices, indices] of int: flows;
array [indices, indices] of int: distances;

% had12.dat
% flows = [|0,  1,  2,  2,  3,  4,  4,  5,  3,  5,  6,  7,
%          |1,  0,  1,  1,  2,  3,  3,  4,  2,  4,  5,  6,
%          |2,  1,  0,  2,  1,  2,  2,  3,  1,  3,  4,  5,
%          |2,  1,  2,  0,  1,  2,  2,  3,  3,  3,  4,  5,
%          |3,  2,  1,  1,  0,  1,  1,  2,  2,  2,  3,  4,
%          |4,  3,  2,  2,  1,  0,  2,  3,  3,  1,  2,  3,
%          |4,  3,  2,  2,  1,  2,  0,  1,  3,  1,  2,  3,
%          |5,  4,  3,  3,  2,  3,  1,  0,  4,  2,  1,  2,
%          |3,  2,  1,  3,  2,  3,  3,  4,  0,  4,  5,  6,
%          |5,  4,  3,  3,  2,  1,  1,  2,  4,  0,  1,  2,
%          |6,  5,  4,  4,  3,  2,  2,  1,  5,  1,  0,  1,
%          |7,  6,  5,  5,  4,  3,  3,  2,  6,  2,  1,  0|];
% distances = [|0,  3,  4,  6,  8,  5,  6,  6,  5,  1,  4,  6,
%              |3,  0,  6,  3,  7,  9,  9,  2,  2,  7,  4,  7,
%              |4,  6,  0,  2,  6,  4,  4,  4,  2,  6,  3,  6,
%              |6,  3,  2,  0,  5,  5,  3,  3,  9,  4,  3,  6,
%              |8,  7,  6,  5,  0,  4,  3,  4,  5,  7,  6,  7,
%              |5,  9,  4,  5,  4,  0,  8,  5,  5,  5,  7,  5,
%              |6,  9,  4,  3,  3,  8,  0,  6,  8,  4,  6,  7,
%              |6,  2,  4,  3,  4,  5,  6,  0,  1,  5,  5,  3,
%              |5,  2,  2,  9,  5,  5,  8,  1,  0,  4,  5,  2,
%              |1,  7,  6,  4,  7,  5,  4,  5,  4,  0,  7,  7,
%              |4,  4,  3,  3,  6,  7,  6,  5,  5,  7,  0,  9,
%              |6,  7,  6,  6,  7,  5,  7,  3,  2,  7,  9,  0|];

% rou12.dat
flows = [|0, 79, 32, 57, 68, 99, 97, 80, 90, 10, 11, 49,
         |79,  0, 96, 62, 55, 11, 79, 17, 28, 88, 62, 32,
         |32, 96,  0, 89, 21, 33,  4, 26, 75, 78, 22, 45,
         |57, 62, 89,  0, 23, 57, 68, 66, 32, 15, 12, 69,
         |68, 55, 21, 23,  0, 33, 84, 54, 95,  5, 15, 10,
         |99, 11, 33, 57, 33,  0, 14, 86, 29, 53, 97, 75,
         |97, 79,  4, 68, 84, 14,  0, 95, 74, 15, 85, 56,
         |80, 17, 26, 66, 54, 86, 95,  0, 34, 38, 79, 27,
         |90, 28, 75, 32, 95, 29, 74, 34,  0, 22, 80, 43,
         |10, 88, 78, 15,  5, 53, 15, 38, 22,  0, 41, 20,
         |11, 62, 22, 12, 15, 97, 85, 79, 80, 41,  0, 55,
         |49, 32, 45, 69, 10, 75, 56, 27, 43, 20, 55,  0|];
distances = [| 0, 78, 22, 43, 86,  8, 99,  5, 32, 89, 19, 69,
             |78,  0,  2, 81, 24, 83, 92, 36, 31, 73, 96,  5,
             |22,  2,  0, 38, 50, 32, 66, 73,  6,  8, 68, 16,
             |43, 81, 38,  0, 53, 75, 40,  8, 63, 30, 30, 10,
             |86, 24, 50, 53,  0, 41, 29, 68, 52, 83, 51, 52,
             | 8, 83, 32, 75, 41,  0, 68, 44,  0, 56, 82, 23,
             |99, 92, 66, 40, 29, 68,  0, 46, 64, 79,  4, 64,
             | 5, 36, 73,  8, 68, 44, 46,  0, 74, 19, 56, 34,
             |32, 31,  6, 63, 52,  0, 64, 74,  0,  2, 14, 95,
             |89, 73,  8, 30, 83, 56, 79, 19,  2,  0, 43, 49,
             |19, 96, 68, 30, 51, 82,  4, 56, 14, 43,  0,  8,
             |69,  5, 16, 10, 52, 23, 64, 34, 95, 49,  8,  0|];

constraint alldifferent(assigned_facilities);

var int: cost = sum(i in indices, j in indices)(flows[i,j] * distances[assigned_facilities[i], assigned_facilities[j]]);

output [ "assigned_facilities = \(assigned_facilities)\n" ++ "cost = \(cost)\n" ];

solve minimize cost;