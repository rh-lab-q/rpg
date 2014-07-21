class SourceLoader:
    def __init__(self, tmp_dir):
        """tmp_dir is path to directory where source archives
           will be extracted"""
        self.source_dir = tmp_dir

    def load_sources(self, file_or_dir, source_dir):
        """extracts archive to source_dir and adds eventually root directory
           if argument is file, changes source_dir to file_or_dir otherwise"""
        pass
