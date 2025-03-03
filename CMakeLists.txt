cmake_minimum_required(VERSION 3.17.0)

project(game_of_stones)

list(APPEND CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake)

find_package(Criterion REQUIRED)

enable_testing()

add_subdirectory(src/)
add_subdirectory(tests/)

set_target_properties(${PROJECT_NAME} PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR})