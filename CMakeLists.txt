cmake_minimum_required(VERSION 3.28)

project(lua-cpp-codegen)

set(CMAKE_CXX_STANDARD 17)

add_subdirectory(lua)
add_subdirectory(sol2)
add_subdirectory(src)

#target_include_directories(launcher PUBLIC ${CMAKE_SOURCE_DIR}/sol2)
set_target_properties(launcher PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR})