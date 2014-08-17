from rpg.plugin import Plugin
import subprocess


class FindPatchPlugin(Plugin):

    def before_patches_applied(self, project_dir, spec, sack):
        patches = [(f, f.stat().st_mtime) for f in project_dir.iterdir()
                   if _is_patch(f)]
        patches_by_modification = sorted(patches, key=lambda m: m[1])
        spec.tags["Patch"] = list(
            map(lambda p: str(p[0]), patches_by_modification))


def _is_patch(path):
    if path.is_dir():
        return False
    output = subprocess.check_output(["file", str(path), "-b"])
    return output.decode().find("unified diff output") != -1
