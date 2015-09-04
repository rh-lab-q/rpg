from rpg.command import Command
from rpg.plugin import Plugin
from javapackages.maven.artifact import Artifact
from javapackages.maven.artifact import ArtifactFormatException
from javapackages.maven.artifact import ArtifactValidationException
from lxml import etree
import logging


class MavenPlugin(Plugin):

    def patched(self, project_dir, spec, sack):
        if (project_dir / "pom.xml").is_file():
            logging.debug('pom.xml found')
            spec.BuildRequires.add("maven-local")
            spec.build = Command('%mvn_build -f')
            install = Command()
            install.append('xmvn-install -R .xmvn-reactor -n ' +
                           spec.Name + ' -d "$RPM_BUILD_ROOT"')
            install.append('jdir=target/site/apidocs; [ -d .xmvn/apidocs ] '
                           '&& jdir=.xmvn/apidocs; '
                           'if [ -d "${jdir}" ]; then '
                           'install -dm755 "$RPM_BUILD_ROOT"/usr/share/'
                           'javadoc/' + spec.Name + '; '
                           'cp -pr "${jdir}"/* "$RPM_BUILD_ROOT"/usr/share/'
                           'javadoc/' + spec.Name + '; '
                           'echo \'/usr/share/javadoc/' + spec.Name +
                           '\' >>.mfiles-javadoc; fi')
            spec.install = install

    def compiled(self, project_dir, spec, sack):
        if(project_dir / ".xmvn-builddep").is_file():
            try:
                et = etree.parse(str(project_dir / ".xmvn-builddep")).getroot()
                deps = et.findall('./dependency')
                for dep in deps:
                    art = Artifact.from_xml_element(dep)
                    spec.BuildRequires.add(art.get_rpm_str(art.version))
            except (ArtifactValidationException,
                    ArtifactFormatException) as e:
                logging.warning("Exception during maven dependency generation"
                                "{e}: Provided artifact strings were invalid."
                                .format(e=e))
                return
