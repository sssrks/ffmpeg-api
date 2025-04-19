{ pkgs }: {
  # Re-deploying manually
  deps = [
    pkgs.ffmpeg
    pkgs.python311
    pkgs.python311Packages.flask
  ];
}
