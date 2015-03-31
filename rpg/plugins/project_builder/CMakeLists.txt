FILE (GLOB rpg_proj_builder_srcs *.py)
INSTALL (FILES ${rpg_proj_builder_srcs} DESTINATION ${PYTHON_INSTALL_DIR}/rpg/plugins/project_builder)
