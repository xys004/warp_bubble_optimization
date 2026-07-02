(* Diagnose cell contents for domain 2 notebook *)
$csvDir = "C:\\Users\\Nelson\\Downloads\\Astrum Drive\\Warp Drive\\Manuscripts\\Dynamic-Warp-Drive-Geometries-from-Static-Bubble-Configurations-Energy-Condition\\notebooks\\";
$nbPath = $csvDir <> "energy_conditions_visual_domain_2.nb";

$nb = Import[$nbPath, "NB"];

(* Extract ALL cells including non-Input types *)
$allCells = Cases[$nb, Cell[___], Infinity];
Print["Total cells: " <> ToString[Length[$allCells]]];

(* Extract Input cells with their indices *)
$inputCells = Cases[$nb, Cell[BoxData[code_], "Input", ___] :> code, Infinity];
Print["Input cells (BoxData): " <> ToString[Length[$inputCells]]];

(* Show first 200 chars of each cell 20-29 *)
Do[
  With[{cellCode = $inputCells[[i]]},
    Print["=== Cell " <> ToString[i] <> " ==="];
    Print[StringTake[ToString[cellCode, InputForm], Min[300, StringLength[ToString[cellCode, InputForm]]]]];
    Print[""]
  ],
  {i, 20, Min[29, Length[$inputCells]]}
];
