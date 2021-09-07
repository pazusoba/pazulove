cmake_minimum_required (VERSION 3.10)

project(
    pazulove
    VERSION 0.1.0
    HOMEPAGE_URL https://github.com/HenryQuan/pazulove
    DESCRIPTION "Using 愛(AI) to solve Puzzle & Dragons"
)

add_subdirectory(pazusoba EXCLUDE_FROM_ALL)
set_target_properties(
    pazuauto
    PROPERTIES
    OUTPUT_NAME "pazulove"
    SUFFIX ".so"
    LIBRARY_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/data\ generation"
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/data\ generation"
)
