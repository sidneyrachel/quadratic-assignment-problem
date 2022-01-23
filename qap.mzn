include "alldifferent.mzn";

int: n;
array [1..n] of var 1..n: assigned_facilities;
set of int: indices = 1..n;
array [indices, indices] of int: flows;
array [indices, indices] of int: distances;  

constraint alldifferent(assigned_facilities);

var int: cost = sum(i in indices, j in indices)(flows[i,j] * distances[assigned_facilities[i], assigned_facilities[j]]);

output [ "assigned_facilities = \(assigned_facilities)\n" ++ "cost = \(cost)\n" ];

solve minimize cost;