link_directories(${LIB_DIR})

link_libraries(tgcreator
                util
                sensors
                core    
                terrain 
                tgOpenGLSupport
        yaml-cpp
		TensegrityModel)

add_executable(AppisocDarYAMLdir
    AppisocDarYAMLdir.cpp
    LengthControllerdarYAMLdir.cpp
    
) 

