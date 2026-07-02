(* Test C compilation via MSYS2 UCRT64 GCC *)
Print["Testing C compilation with MSYS2 GCC..."];

(* Add MSYS2 UCRT64 to PATH so Mathematica's CCompilerDriver finds gcc *)
$oldPath = Environment["PATH"];
SetEnvironmentVariable["PATH", "C:\\msys64\\ucrt64\\bin;" <> $oldPath];

Needs["CCompilerDriver`"];

(* List available compilers *)
Print["Available compilers: " <> ToString[CCompilers[]]];

(* Try compiling a simple function *)
testF = Compile[{{x, _Real}}, x^2 + 1.0, CompilationTarget -> "C"];
result = testF[3.0];
Print["Compile test: f(3.0) = " <> ToString[result]];
Print["Expected: 10.0"];
Print["Success: " <> ToString[result == 10.0]];
