(* Test GCC compilation via SystemOptions *)
Needs["CCompilerDriver`GCCCompiler`"];

Print["Current CCompilerOptions: " <> ToString[SystemOptions["CCompilerOptions"]]];

(* Set GCC as the default C compiler *)
SetSystemOptions["CCompilerOptions" -> {
  "Compiler" -> CCompilerDriver`GCCCompiler`GCCCompiler,
  "CompilerInstallation" -> "C:\\msys64\\ucrt64\\bin",
  "CompilerName" -> "gcc"
}];

Print["After setting GCC:"];
Print[SystemOptions["CCompilerOptions"]];

(* Test compilation *)
Print["Compiling test function..."];
testF = Compile[{{x, _Real}}, x^2 + 1.0, CompilationTarget -> "C"];
Print["Result: " <> ToString[testF[3.0]]];
Print["Expected: 10."];
