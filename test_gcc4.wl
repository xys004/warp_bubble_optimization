(* Try GCC from PATH only, no explicit CompilerInstallation *)
Needs["CCompilerDriver`"];
Needs["CCompilerDriver`GCCCompiler`"];

Print["PATH has gcc? " <> ToString[FindFile["gcc"]]];

srcFile = Export[FileNameJoin[{$TemporaryDirectory, "test3.c"}],
  "double sq1(double x) { return x*x + 1.0; }", "Text"];

(* No CompilerInstallation - let it find from PATH *)
Print["Trying without explicit CompilerInstallation..."];
result = CCompilerDriver`CreateLibrary[srcFile, "testlib3",
  "Compiler" -> CCompilerDriver`GCCCompiler`GCCCompiler
];
Print["Library: " <> ToString[result]];

(* Also list what CCompilers detects *)
Print["Detected compilers: " <> ToString[CCompilers[]]];
