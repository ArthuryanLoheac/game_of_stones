file(GLOB_RECURSE TEST_SRC "./**.cpp" "../src/**.cpp")

add_executable(unit_tests ${TEST_SRC})

include_directories(${CMAKE_SOURCE_DIR}/include)
file(GLOB_RECURSE HEADER_FILES "../include/**.hpp")

foreach(HEADER_FILE ${HEADER_FILES})
    get_filename_component(HEADER_DIR ${HEADER_FILE} DIRECTORY)
    include_directories(${HEADER_DIR})
endforeach()

target_include_directories(unit_tests PRIVATE ${CRITERION_INCLUDE_DIRS})
target_link_libraries(unit_tests ${CRITERION_LIBRARIES})
set_target_properties(unit_tests PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})
add_test(NAME unit_tests COMMAND unit_tests)