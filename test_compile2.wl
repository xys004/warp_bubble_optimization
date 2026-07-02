(* Test explicit VS compiler configuration *)
Needs["CCompilerDriver`"];
Needs["CCompilerDriver`VisualStudioCompiler`"];

Print["Trying explicit VisualStudio compiler..."];

(* Use explicit compiler with x64 cl.exe *)
\$vsVer = "14.42.34433";
\$clPath = "C:\\Program Files (x86)\\Microsoft Visual Studio\\2022\\BuildTools\\VC\\Tools\\MSVC\\" <> \$vsVer <> "\\bin\\Hostx64\\x64";

(* Also need the Windows SDK - check if it's there *)
\$sdkDirs = FileNames["*", "C:\\Program Files (x86)\\Windows Kits\\10\\Include"];
Print["Windows SDK Include dirs: " <> ToString[\$sdkDirs]];

(* Try with explicit compiler installation path *)
testF = Compile[{{x, _Real}}, x^2 + 1.0,
  CompilationTarget -> "C",
  "CompilerInstallation" -> "C:\\Program Files (x86)\\Microsoft Visual Studio\\2022\\BuildTools"
];
result = testF[3.0];
Print["Result: " <> ToString[result]];
