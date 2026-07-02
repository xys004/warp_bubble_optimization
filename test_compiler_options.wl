(* Discover the right way to configure compiler in Mathematica 13 *)
Needs["CCompilerDriver`"];
Needs["CCompilerDriver`GCCCompiler`"];

(* Find relevant system options *)
allOpts = SystemOptions[];
compileOpts = Select[allOpts, StringContainsQ[ToString[#[[1]]], "Compil", IgnoreCase->True] &];
Print["Compile-related options: " <> ToString[compileOpts]];

(* Try CreateLibrary directly with GCC *)
Print["\nTrying CreateLibrary with GCC..."];
srcFile = Export[FileNameJoin[{$TemporaryDirectory, "test.c"}], "
#include <math.h>
double square_plus_one(double x) { return x*x + 1.0; }
", "Text"];
Print["Source: " <> srcFile];

result = CCompilerDriver`CreateLibrary[srcFile, "testlib_gcc",
  "Compiler" -> CCompilerDriver`GCCCompiler`GCCCompiler,
  "CompilerInstallation" -> "C:\\msys64\\ucrt64\\bin",
  "CompilerName" -> "gcc"
];
Print["Library: " <> ToString[result]];
