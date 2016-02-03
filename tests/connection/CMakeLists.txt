FILE (GLOB files test_*.py)
FOREACH (file ${files})
    ADD_TEST(${file} ${NOSETESTS_EXE} ${file} -w ${PROJECT_SOURCE_DIR})
ENDFOREACH ()

