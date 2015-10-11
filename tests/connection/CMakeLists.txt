FILE (GLOB files test_*.py)
FOREACH (file ${files})
    ADD_TEST(${file} nosetests-3.4 ${file} -w ${PROJECT_SOURCE_DIR})
ENDFOREACH ()

