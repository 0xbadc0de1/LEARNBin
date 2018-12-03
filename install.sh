wget https://github.com/BinaryAnalysisPlatform/bap/releases/download/v1.4.0/{bap,libbap,libbap-dev}_1.4.0.deb
sudo dpkg -i {bap,libbap,libbap-dev}_1.4.0.deb
sh <(curl -sL https://raw.githubusercontent.com/ocaml/opam/master/shell/install.sh)
opam init --comp=4.05.0              # install the compiler
eval `opam config env`               # activate opam environment
opam depext --install bap            # install bap
