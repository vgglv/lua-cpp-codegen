file(GLOB_RECURSE SOURCES "*.cpp" "*.hpp")

add_executable(launcher ${SOURCES})

target_link_libraries(launcher PUBLIC lua)