{
  description = "Python Development Environment with PyCharm Professional";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = import nixpkgs { inherit system; };
      python = pkgs.python3;

      # Create a dedicated virtual environment
      venv = pkgs.python3.withPackages (ps: with ps; [ 
        black
        flake8
        mypy
        pytest
      ]);

      # PyCharm Professional with bundled JDK
      pycharm = pkgs.jetbrains.pycharm-professional;

    in {
      # Simple development shell with the specified packages
      devShells.default = pkgs.mkShell {
        buildInputs = [
          python
          venv
          pycharm
        ];
        shellHook = ''
          export PYCHARM_PYTHON_PATH="${python}";
          pycharm-professional
        '';
      };

      # Expose environment variables (optional)
      # You can customize these as needed for your projects
      env = {
        PYTHONUNBUFFERED = 1;
        PYTHON_INTERPRETER = venv; 
      };
    });
}
