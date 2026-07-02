(* Debug: check what gets defined after Get *)
$csvDir = "C:\\Users\\Nelson\\Downloads\\Astrum Drive\\Warp Drive\\Manuscripts\\Dynamic-Warp-Drive-Geometries-from-Static-Bubble-Configurations-Energy-Condition\\notebooks\\";
$nbPath = $csvDir <> "energy_conditions_visual_domain_2.nb";

Unprotect[NotebookDirectory];
NotebookDirectory[] := $csvDir;
Protect[NotebookDirectory];

Unprotect[Row];
Row[args___] := Null;
Protect[Row];

Get[$nbPath];

Print["a = ", a];
Print["b = ", b];
Print["R0 = ", R0];
Print["pairsXZ defined? ", ValueQ[pairsXZ]];
Print["pairsXY defined? ", ValueQ[pairsXY]];
Print["createDensityPlot defined? ", ValueQ[createDensityPlot]];
Print["plotsXZ length: ", Length[plotsXZ]];
Print["plotsXY length: ", Length[plotsXY]];
