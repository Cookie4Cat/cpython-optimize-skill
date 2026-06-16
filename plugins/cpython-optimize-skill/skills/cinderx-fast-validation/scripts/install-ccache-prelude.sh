#!/usr/bin/env bash
set -euo pipefail

prelude_path="${CINDERX_CCACHE_PRELUDE_PATH:-$HOME/cinderx-setup-release-ccache-prelude.sh}"

mkdir -p "$(dirname "$prelude_path")"

cat > "$prelude_path" <<'SCRIPT'
# Enable ccache only for:
# - cinderx_local.setup_release, identified by CINDERX_INCLUDE_TEST_PACKAGE_DATA=1
# - explicit manual wheel builds, identified by CINDERX_CCACHE_FORCE=1
#
# Keep the manual switch explicit so runtime_tests and unrelated CMake builds do
# not inherit CCACHE_BASEDIR or compiler wrappers accidentally.
if { [ "${CINDERX_INCLUDE_TEST_PACKAGE_DATA:-}" = "1" ] || [ "${CINDERX_CCACHE_FORCE:-}" = "1" ]; } && command -v ccache >/dev/null 2>&1; then
  wrapper_dir="${CINDERX_CCACHE_WRAPPER_DIR:-/tmp/cinderx-ccache-wrappers}"
  ccache_bin="$(command -v ccache)"

  mkdir -p "$wrapper_dir"
  ln -sf "$ccache_bin" "$wrapper_dir/gcc"
  ln -sf "$ccache_bin" "$wrapper_dir/g++"

  export CC="$wrapper_dir/gcc"
  export CXX="$wrapper_dir/g++"
  export CCACHE_DIR="${CINDERX_CCACHE_DIR:-$HOME/.cache/ccache-cinderx}"
  export CCACHE_MAXSIZE="${CINDERX_CCACHE_MAXSIZE:-5G}"
  export CCACHE_COMPILERCHECK="${CCACHE_COMPILERCHECK:-content}"
  export CCACHE_PATH="${CINDERX_CCACHE_PATH:-/usr/local/bin:/opt/gcc-14.2/bin:/usr/bin:/bin}"

  if [ -n "${CINDERX_CCACHE_BASEDIR:-}" ]; then
    export CCACHE_BASEDIR="$CINDERX_CCACHE_BASEDIR"
    export CCACHE_NOHASHDIR="${CCACHE_NOHASHDIR:-1}"
  fi
fi
SCRIPT

chmod 0644 "$prelude_path"

if command -v ccache >/dev/null 2>&1; then
  ccache --version | head -n 1
else
  echo "warning: ccache is not installed or not on PATH; the prelude will be inert until ccache is available" >&2
fi

printf 'installed %s\n' "$prelude_path"
