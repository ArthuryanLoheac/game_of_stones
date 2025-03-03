cmake_minimum_required(VERSION 3.17.0)
project(game_of_stones)
set(CMAKE_CXX_STANDARD 20)

file(GLOB_RECURSE SRCS "./**.cpp" "../main.cpp")
include_directories(${CMAKE_SOURCE_DIR}/include)
file(GLOB_RECURSE HEADER_FILES "../include/**.hpp" "./**.hpp")

foreach(HEADER_FILE ${HEADER_FILES})
    get_filename_component(HEADER_DIR ${HEADER_FILE} DIRECTORY)
    include_directories(${HEADER_DIR})
endforeach()
add_executable(${PROJECT_NAME} ${SRCS})
