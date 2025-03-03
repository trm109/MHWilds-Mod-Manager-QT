{ pkgs, lib, config, inputs, ... }:

{
  # https://devenv.sh/basics/
  #env.GREET = "devenv";

  # https://devenv.sh/packages/
  packages = [
    pkgs.git
    #pkgs.libsForQt5.qt5.qtwayland
    pkgs.electron
    pkgs.autoPatchelfHook
    pkgs.python312Packages.pyqt6
    pkgs.python312Packages.pyside6
  ];

  # https://devenv.sh/languages/
  languages.python = {
    enable = true;
    package = pkgs.python312Full;
    uv = {
      enable = true;
      sync.enable = true;
    };
    libraries = [
      pkgs.python312Packages.pyqt6
    ];
  };

  # https://devenv.sh/processes/
  # processes.cargo-watch.exec = "cargo-watch";

  # https://devenv.sh/services/
  # services.postgres.enable = true;

  # https://devenv.sh/scripts/
  #scripts.hello.exec = ''
  #  echo hello from $GREET
  #'';

  enterShell = ''
    git fetch
    export LD_LIBRARY_PATH=${pkgs.libGL}/lib/:${pkgs.libxkbcommon}/lib/:${pkgs.fontconfig.lib}/lib/:${pkgs.xorg.libX11.out}/lib/:${pkgs.glib.out}/lib/:${pkgs.libz.out}/lib/:${pkgs.freetype.out}/lib/:${pkgs.zstd.out}/lib/:${pkgs.dbus.lib}/lib/
  '';

  # https://devenv.sh/tasks/
  # tasks = {
  #   "myproj:setup".exec = "mytool build";
  #   "devenv:enterShell".after = [ "myproj:setup" ];
  # };

  # https://devenv.sh/tests/
  enterTest = ''
    echo "No tests yet"
  '';

  # https://devenv.sh/git-hooks/
  # git-hooks.hooks.shellcheck.enable = true;
  git-hooks.hooks = {
    black = {
      enable = true;
    };
  };

  # See full reference at https://devenv.sh/reference/options/
}
