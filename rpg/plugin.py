class Plugin:

    """class from which are plugins derived"""

    def before_patches_aplied(self, project_dir, spec, sack):
        # :api
        pass

    def after_patches_applied(self, project_dir, spec, sack):
        # :api
        pass

    def after_project_build(self, project_dir, spec, sack):
        # :api
        pass
