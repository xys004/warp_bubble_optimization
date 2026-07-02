(* Verbose compilation test *)
Needs["CCompilerDriver`"];
Needs["CCompilerDriver`GCCCompiler`"];

srcFile = Export[FileNameJoin[{$TemporaryDirectory, "test4.c"}],
  "double sq1(double x) { return x*x + 1.0; }", "Text"];

(* Enable verbose output *)
Print["=== GCC test ==="];
result = CCompilerDriver`CreateLibrary[srcFile, "testlib4",
  "Compiler" -> CCompilerDriver`GCCCompiler`GCCCompiler,
  "CompilerInstallation" -> "C:\\msys64\\ucrt64\\bin",
  "CompilerName" -> "gcc",
  "ShellCommandFunction" -> Print,
  "ShellOutputFunction" -> Print
];
Print["GCC result: " <> ToString[result]];

Print["\n=== VS test ==="];
result2 = CCompilerDriver`CreateLibrary[srcFile, "testlib4vs",
  "Compiler" -> CCompilerDriver`VisualStudioCompiler`VisualStudioCompiler,
  "ShellCommandFunction" -> Print,
  "ShellOutputFunction" -> Print
];
Print["VS result: " <> ToString[result2]];
