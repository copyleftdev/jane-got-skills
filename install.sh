#!/usr/bin/env bash
# Install the skills in this repo into Claude Code by symlinking skills/<name> into the skills dir.
#
# usage: ./install.sh [--dir DIR] [--force] [--list | --uninstall] [skill ...]
#   --dir DIR     target directory (default: $CLAUDE_SKILLS_DIR or ~/.claude/skills)
#   --force       replace an existing symlink of the same name that points elsewhere
#   --list        show each skill's status without changing anything
#   --uninstall   remove only symlinks that point into this repo
#   skill ...     limit to these skill directory names (default: all)
#
# Never removes or overwrites a real file or directory. Exit status 1 if anything was left in conflict.
set -euo pipefail

repo=$(cd "$(dirname "$0")" && pwd)
dir=${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}
mode=install force=0 picked=()
while (($#)); do
  case $1 in
    --dir) dir=$2; shift 2 ;;
    --force) force=1; shift ;;
    --list) mode=list; shift ;;
    --uninstall) mode=uninstall; shift ;;
    -h|--help) sed -n '2,11p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    -*) echo "unknown option: $1" >&2; exit 2 ;;
    *) picked+=("$1"); shift ;;
  esac
done

skills=()
for d in "$repo"/skills/*/; do
  name=$(basename "$d")
  [[ -f $d/SKILL.md ]] || continue
  if ((${#picked[@]})) && [[ ! " ${picked[*]} " == *" $name "* ]]; then continue; fi
  skills+=("$name")
done
for p in "${picked[@]+"${picked[@]}"}"; do
  [[ -f $repo/skills/$p/SKILL.md ]] || { echo "no such skill: $p" >&2; exit 2; }
done

frontmatter_name() { awk '/^---$/{n++; next} n==1 && /^name:/{sub(/^name:[ \t]*/, ""); print; exit}' "$1"; }

[[ $mode == list ]] || mkdir -p "$dir"
conflicts=0
for name in "${skills[@]}"; do
  src="$repo/skills/$name"
  dst="$dir/$name"
  label="$name ($(frontmatter_name "$src/SKILL.md"))"
  if [[ -z $(frontmatter_name "$src/SKILL.md") ]]; then
    echo "invalid  $name: SKILL.md has no name: in its frontmatter"; conflicts=1; continue
  fi
  current=""
  [[ -L $dst ]] && current=$(readlink "$dst")
  case $mode in
    list)
      if [[ $current == "$src" ]]; then echo "installed     $label"
      elif [[ -L $dst ]]; then echo "other link    $label -> $current"
      elif [[ -e $dst ]]; then echo "conflict      $label (a real file or directory is in the way)"
      else echo "not installed $label"; fi ;;
    install)
      if [[ $current == "$src" ]]; then echo "ok        $label"
      elif [[ -L $dst ]]; then
        if ((force)); then ln -sfn "$src" "$dst"; echo "replaced  $label (was -> $current)"
        else echo "skipped   $label: $dst links to $current (use --force)"; conflicts=1; fi
      elif [[ -e $dst ]]; then echo "conflict  $label: $dst is a real file or directory; left untouched"; conflicts=1
      else ln -s "$src" "$dst"; echo "linked    $label"; fi ;;
    uninstall)
      if [[ $current == "$src" ]]; then rm "$dst"; echo "removed   $label"
      elif [[ -e $dst || -L $dst ]]; then echo "kept      $label: $dst is not this repo's link"
      else echo "absent    $label"; fi ;;
  esac
done
exit $conflicts
