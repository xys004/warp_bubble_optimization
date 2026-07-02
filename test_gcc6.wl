(* Use auto-detected GCC, no explicit CompilerInstallation *)
Needs["CCompilerDriver`"];
Needs["CCompilerDriver`GCCCompiler`"];

srcFile = Export[FileNameJoin[{$TemporaryDirectory, "test5.c"}],
  "double sq1(double x) { return x*x + 1.0; }", "Text"];

Print["Auto-detect GCC test..."];
result = CCompilerDriver`CreateLibrary[srcFile, "testlib5",
  "Compiler" -> CCompilerDriver`GCCCompiler`GCCCompiler,
  "ShellCommandFunction" -> Print,
  "ShellOutputFunction" -> Print
];
Print["Result: " <> ToString[result]];

(* If that worked, test Compile[] with GCC *)
If[result =!= $Failed,
  Print["Testing Compile[] with GCC..."];
  testF = Compile[{{x, _Real}}, x^2 + 1.0,
    CompilationTarget -> "C",
    "Compiler" -> CCompilerDriver`GCCCompiler`GCCCompiler
  ];
  Print["f(3.0) = " <> ToString[testF[3.0]]]
];
