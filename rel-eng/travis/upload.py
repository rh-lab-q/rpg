from copr.client import CoprClient
import sys

found_project = False
cl = CoprClient(username="nightly", login=sys.argv[1], token=sys.argv[2],
                copr_url="http://copr.fedoraproject.org")
result = cl.get_projects_list("nightly").projects_list
for project in result:
    if project.projectname == "rpg":
        found_project = True
        break
if not found_project:
    chroot = ["fedora-21-x86_64", "fedora-21-i386", "fedora-22-x86_64",
              "fedora-22-i386", "fedora-rawhide-i386", "fedora-rawhide-x86_64"]
    cl.create_project("rpg", chroots=chroot)
srpm_name = 'https://github.com/PavolVican/rpg/raw/srpm/' + sys.argv[3]
cl.create_new_build("rpg", pkgs=[srpm_name])
