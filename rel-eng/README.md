Release instructions
====================

1. Tag: tito tag
2. Push: git push origin HEAD:master && git push origin `git describe --abbrev=0 --tags`
3. Release: tito release fedora-git
