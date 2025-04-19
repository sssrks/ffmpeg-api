{ pkgs }: {
  # This should trigger redeploy
  deps = [
    pkgs.ffmpeg
    pkgs.python311
    pkgs.python311Packages.flask
  ];
}
