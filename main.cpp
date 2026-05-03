
#include "glad/glad.h"
#include <GLFW/glfw3.h>
#include <iostream>
#include <cmath>
#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"

#define STB_IMAGE_WRITE_IMPLEMENTATION 
#include "stb_image_write.h"



void saveScreenshot(int width, int height, const char* filename) {
    unsigned char* pixels = new unsigned char[3 * width * height];
    glReadPixels(0, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE, pixels);
    
    // OpenGL малює знизу вгору, тому треба перевернути зображення
    stbi_flip_vertically_on_write(true);
    stbi_write_png(filename, width, height, 3, pixels, width * 3);
    delete[] pixels;
}

const char *vertexShaderSource = "#version 330 core\n"
    "layout (location = 0) in vec3 aPos;\n"
    "layout (location = 1) in vec2 aTexCoord;\n"
    "out vec2 TexCoord;\n"
    "uniform mat4 transform;\n"
    "void main() {\n"
    "   gl_Position = transform * vec4(aPos, 1.0);\n"
    "   TexCoord = vec2(aTexCoord.x, aTexCoord.y);\n"
    "}\0";

const char *fragmentShaderSource = "#version 330 core\n"
    "out vec4 FragColor;\n"
    "in vec2 TexCoord;\n"
    "uniform sampler2D texture1;\n"
    "void main() {\n"
    "   FragColor = texture(texture1, TexCoord);\n"
    "}\n\0";

// Глобальні змінні для анімації
bool isPaused = false;
bool showTask2 = false; // Натисніть '2' для Завдання 2, '1' для Завдання 1

void processInput(GLFWwindow *window) {
    if (glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS)
        glfwSetWindowShouldClose(window, true);

    // Перемикання завдань
    if (glfwGetKey(window, GLFW_KEY_1) == GLFW_PRESS) showTask2 = false;
    if (glfwGetKey(window, GLFW_KEY_2) == GLFW_PRESS) showTask2 = true;

    // Пауза пробілом (з фіксацією натискання)
    static bool spaceWasPressed = false;
    if (glfwGetKey(window, GLFW_KEY_SPACE) == GLFW_PRESS) {
        if (!spaceWasPressed) {
            isPaused = !isPaused;
            spaceWasPressed = true;
        }
    } else spaceWasPressed = false;
}

unsigned int loadTexture(const char* path) {
    unsigned int textureID;
    glGenTextures(1, &textureID);
    glBindTexture(GL_TEXTURE_2D, textureID);

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);

    int width, height, nrChannels;
    stbi_set_flip_vertically_on_load(true);
    unsigned char *data = stbi_load(path, &width, &height, &nrChannels, 0);
    if (data) {
        GLenum format = (nrChannels == 4) ? GL_RGBA : GL_RGB;
        glTexImage2D(GL_TEXTURE_2D, 0, format, width, height, 0, format, GL_UNSIGNED_BYTE, data);
        glGenerateMipmap(GL_TEXTURE_2D);
    } else {
        std::cout << "Failed to load texture: " << path << std::endl;
    }
    stbi_image_free(data);
    return textureID;
}

int main() {
    glfwInit();
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

    GLFWwindow* window = glfwCreateWindow(800, 600, "Graphics Lab: Textures", NULL, NULL);
    if (!window) { glfwTerminate(); return -1; }
    glfwMakeContextCurrent(window);

    if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress)) return -1;

    // Шейдерна програма
    unsigned int vertexShader = glCreateShader(GL_VERTEX_SHADER);
    glShaderSource(vertexShader, 1, &vertexShaderSource, NULL);
    glCompileShader(vertexShader);
    unsigned int fragmentShader = glCreateShader(GL_FRAGMENT_SHADER);
    glShaderSource(fragmentShader, 1, &fragmentShaderSource, NULL);
    glCompileShader(fragmentShader);
    unsigned int shaderProgram = glCreateProgram();
    glAttachShader(shaderProgram, vertexShader);
    glAttachShader(shaderProgram, fragmentShader);
    glLinkProgram(shaderProgram);
    glDeleteShader(vertexShader);
    glDeleteShader(fragmentShader);

    // Дані для 3 прямокутників (Завдання 1)
    float rectsVertices[] = {
        // Позиції            // Текстури
        -0.9f,  0.5f, 0.0f,   0.0f, 1.0f, // Пр 1
        -0.4f,  0.5f, 0.0f,   1.0f, 1.0f,
        -0.4f, -0.5f, 0.0f,   1.0f, 0.0f,
        -0.9f, -0.5f, 0.0f,   0.0f, 0.0f,

        -0.25f, 0.5f, 0.0f,   0.0f, 1.0f, // Пр 2
         0.25f, 0.5f, 0.0f,   1.0f, 1.0f,
         0.25f,-0.5f, 0.0f,   1.0f, 0.0f,
        -0.25f,-0.5f, 0.0f,   0.0f, 0.0f,

         0.4f,  0.5f, 0.0f,   0.0f, 1.0f, // Пр 3
         0.9f,  0.5f, 0.0f,   1.0f, 1.0f,
         0.9f, -0.5f, 0.0f,   1.0f, 0.0f,
         0.4f, -0.5f, 0.0f,   0.0f, 0.0f
    };
    unsigned int indices[] = { 
        0, 1, 2, 0, 2, 3,       // Rect 1
        4, 5, 6, 4, 6, 7,       // Rect 2
        8, 9, 10, 8, 10, 11     // Rect 3
    };

    // Дані для квадрата (Завдання 2)
    float squareVertices[] = {
         0.3f,  0.3f, 0.0f,   1.0f, 1.0f,
         0.3f, -0.3f, 0.0f,   1.0f, 0.0f,
        -0.3f, -0.3f, 0.0f,   0.0f, 0.0f,
        -0.3f,  0.3f, 0.0f,   0.0f, 1.0f
    };
    unsigned int squareIndices[] = { 0, 1, 3, 1, 2, 3 };

    unsigned int VBO[2], VAO[2], EBO[2];
    glGenVertexArrays(2, VAO); glGenBuffers(2, VBO); glGenBuffers(2, EBO);

    // Налаштування для прямокутників
    glBindVertexArray(VAO[0]);
    glBindBuffer(GL_ARRAY_BUFFER, VBO[0]);
    glBufferData(GL_ARRAY_BUFFER, sizeof(rectsVertices), rectsVertices, GL_STATIC_DRAW);
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO[0]);
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(indices), indices, GL_STATIC_DRAW);
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5 * sizeof(float), (void*)0);
    glEnableVertexAttribArray(0);
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5 * sizeof(float), (void*)(3 * sizeof(float)));
    glEnableVertexAttribArray(1);

    // Налаштування для квадрата
    glBindVertexArray(VAO[1]);
    glBindBuffer(GL_ARRAY_BUFFER, VBO[1]);
    glBufferData(GL_ARRAY_BUFFER, sizeof(squareVertices), squareVertices, GL_STATIC_DRAW);
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO[1]);
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(squareIndices), squareIndices, GL_STATIC_DRAW);
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5 * sizeof(float), (void*)0);
    glEnableVertexAttribArray(0);
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5 * sizeof(float), (void*)(3 * sizeof(float)));
    glEnableVertexAttribArray(1);

    unsigned int tex1 = loadTexture("tex1.jpg"); 
    unsigned int tex2 = loadTexture("tex2.jpg"); 
    unsigned int tex3 = loadTexture("tex3.jpg"); 

    glUseProgram(shaderProgram);
    
    double lastTime = glfwGetTime();
    float rotation = 0.0f;

    while (!glfwWindowShouldClose(window)) {
        double currentTime = glfwGetTime();
        // 2.4 Обмеження 60 FPS
        if (currentTime - lastTime >= 1.0 / 60.0) {
            float deltaTime = (float)(currentTime - lastTime);
            lastTime = currentTime;

            processInput(window);
            glClearColor(0.1f, 0.1f, 0.1f, 1.0f);
            glClear(GL_COLOR_BUFFER_BIT);

            unsigned int transformLoc = glGetUniformLocation(shaderProgram, "transform");

            if (!showTask2) {
                // --- ЗАВДАННЯ 1 ---
                float identity[16] = { 1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1 };
                glUniformMatrix4fv(transformLoc, 1, GL_FALSE, identity);
                glBindVertexArray(VAO[0]);
                
                glBindTexture(GL_TEXTURE_2D, tex1);
                glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0);
                
                glBindTexture(GL_TEXTURE_2D, tex2);
                glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, (void*)(6 * sizeof(unsigned int)));
                
                glBindTexture(GL_TEXTURE_2D, tex3);
                glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, (void*)(12 * sizeof(unsigned int)));
            } else {
                // --- ЗАВДАННЯ 2 ---
                if (!isPaused) rotation += deltaTime * 2.0f;
                float c = cos(rotation); float s = sin(rotation);
                float rotateZ[16] = {
                    c, s, 0, 0,
                   -s, c, 0, 0,
                    0, 0, 1, 0,
                    0, 0, 0, 1
                };
                glUniformMatrix4fv(transformLoc, 1, GL_FALSE, rotateZ);
                glBindVertexArray(VAO[1]);
                glBindTexture(GL_TEXTURE_2D, tex1);
                glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0);
            }

            glfwSwapBuffers(window);
            glfwPollEvents();
   
saveScreenshot(800, 600, "task1_result.png");
std::cout << "Screenshot saved to task1_result.png!" << std::endl;
glfwSetWindowShouldClose(window, true); 
        }
    }
    glfwTerminate();
    return 0;
}

