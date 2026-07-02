(* Fix: CompilerInstallation should be root, not bin subdir *)
Needs["CCompilerDriver`"];
Needs["CCompilerDriver`GCCCompiler`"];

srcFile = Export[FileNameJoin[{$TemporaryDirectory, "test2.c"}],
  "double square_plus_one(double x) { return x*x + 1.0; }", "Text"];

(* Try root of ucrt64 *)
Print["Trying CompilerInstallation -> C:\\msys64\\ucrt64 ..."];
result = CCompilerDriver`CreateLibrary[srcFile, "testlib2",
  "Compiler" -> CCompilerDriver`GCCCompiler`GCCCompiler,
  "CompilerInstallation" -> "C:\\msys64\\ucrt64",
  "CompilerName" -> "gcc"
];
Print["Library result: " <> ToString[result]];
