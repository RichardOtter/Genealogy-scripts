# ReadMe Build Workflow

The documentation scripts build project ReadMe files in a staging folder so
they can be reviewed before being copied into the project folders.

## Files and configuration

Paths below are relative to the repository root.

| Path | Purpose |
| --- | --- |
| `doc\doc-sources\DocOutline_{project}.txt` | Source template for each project |
| `doc\docs-reusable-content.txt` | Shared text inserted by INCLUDE directives |
| `doc\docs-generated\ReadMe_{project}.txt` | Generated ReadMe for review |
| `{project}\ReadMe.txt` | Project copy of the ReadMe |
| `dev util scripts\projects-to-build.yaml` | Project list and suite version |
| `dev util scripts\Build doc\` | Documentation scripts |

The scripts use `ProjectList` in the configuration file. Each listed project
needs a matching source template and project folder. The build also reads the
utility version from the project's `_util_info.yaml`; if it is missing, the
generated footer uses `Unknown`.

Both build scripts require `BuildType` to be exactly `DEV`, `ALPHA`, `BETA`,
or `RELEASE`. A missing, blank, or other value stops the build with an error
before output files are changed.

The scripts require Python and PyYAML. The build and discard scripts also
require `send2trash`; the copy script uses it if installed. The discard
script requires Git.

## Build and review

Run these commands from the repository root:

1. Edit the appropriate template in `doc\doc-sources`, or edit shared text in
   `doc\docs-reusable-content.txt`.

2. Build the staged files:

   ```powershell
   py "dev util scripts\Build doc\Build ReadMe files.py"
   ```

   The build expands INCLUDE directives, substitutes template variables,
   omits the variables section, and adds suite version, utility version, and
   build date information. Shared lines are prefixed with `╋` for `DEV` and
   `ALPHA`, but not for `BETA` or `RELEASE`. The build type is appended to
   the versions unless it is `RELEASE`. The suite release builder likewise
   includes `DEV`, `ALPHA`, or `BETA` in distribution names and utility
   versions, but omits `RELEASE`.

   **The build first sends every existing file directly inside
   `doc\docs-generated` to the Recycle Bin**, then generates the configured
   projects. Do not keep unrelated files there. If an error occurs, the
   staging folder may contain only part of the output; check the console and
   rebuild before copying. The build script can print an error without
   returning a failing process exit code.

3. Review the staged `ReadMe_{project}.txt` files in `doc\docs-generated`.
   Check for unresolved directives, incorrect content, and formatting. Edit
   the source template or shared content and rebuild if changes are needed.

4. Once satisfied, copy all configured staged files to their project folders:

   ```powershell
   py "dev util scripts\Build doc\Copy-ReadMe-to-Projects.py"
   ```

   This replaces each `{project}\ReadMe.txt`, including any local changes.
   Existing files are sent to the Recycle Bin if `send2trash` is available;
   otherwise they are deleted. The script stops on the first error, so an
   incomplete run may have already replaced some project files. Review the
   console output and Git changes after copying.

## Read-only protection

Generated files are intended for review, not direct editing:

- The build sets the Windows read-only file attribute on each generated
  ReadMe and adds `doc/docs-generated/**` to `files.readonlyInclude` in the
  repository's `.vscode\settings.json`.
- The copy preserves the file attribute and adds each configured project
  `ReadMe.txt` to the same VS Code setting. If the settings update fails, the
  copy script prints a warning; the copies may already exist.

The VS Code setting makes matching files read-only in the editor; the Windows
file attribute is separate and also affects writes outside VS Code. To make
lasting changes, edit the source template or shared content and rebuild,
rather than editing the generated or copied file. Removing the VS Code
setting alone does not clear the Windows attribute, and running the scripts
adds their settings and attributes again.

Both scripts update `.vscode\settings.json`, preserving settings they can
parse. The file must contain valid JSON for the scripts to read it.

## Discard project ReadMe changes

To restore the configured project ReadMe files from Git's **index**:

```powershell
py "dev util scripts\Build doc\Discard-ReadMe-Changes.py"
```

**Review `git status` first.** This operates on every configured project's
ReadMe, including unrelated local edits. When Git reports changes and the
file exists, the script sends it to the Recycle Bin before running
`git checkout` for that path. Checkout restores the index version, not
necessarily the last commit: staged changes remain staged and are restored
to the working file. The script stops on the first error; earlier files may
already have been processed. A file absent from the Git index cannot be
restored this way.

Discarding project copies does not revert templates or shared content and
does not undo a build in `doc\docs-generated`.
