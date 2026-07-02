nb1path = "C:\\Users\\Nelson\\Downloads\\Astrum Drive\\Warp Drive\\Manuscripts\\Dynamic-Warp-Drive-Geometries-from-Static-Bubble-Configurations-Energy-Condition\\notebooks\\energy_conditions_visual_domain_1.nb";
nb2path = "C:\\Users\\Nelson\\Downloads\\Astrum Drive\\Warp Drive\\Manuscripts\\Dynamic-Warp-Drive-Geometries-from-Static-Bubble-Configurations-Energy-Condition\\notebooks\\energy_conditions_visual_domain_2.nb";
outdir = "C:\\Users\\Nelson\\Downloads\\warp_optimization\\";

Print["Converting domain_1..."];
Export[outdir <> "run_domain_1.wl", Import[nb1path], "Package"];
Print["Domain 1 done."];

Print["Converting domain_2..."];
Export[outdir <> "run_domain_2.wl", Import[nb2path], "Package"];
Print["Domain 2 done."];
