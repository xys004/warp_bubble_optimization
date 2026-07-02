(* Test GCC compilation via MSYS2 *)
Needs["CCompilerDriver`GCCCompiler`"];

Print["Testing GCC..."];
Print["GCC path: " <> ToString[FindFile["gcc"]]];

testF = Compile[{{x, _Real}}, x^2 + 1.0,
  CompilationTarget -> "C",
  "Compiler" -> CCompilerDriver`GCCCompiler`GCCCompiler,
  "CompilerInstallation" -> "C:\\msys64\\ucrt64\\bin",
  "CompilerName" -> "gcc"
];
Print["Result: " <> ToString[testF[3.0]]];
Print["Expected: 10."];
