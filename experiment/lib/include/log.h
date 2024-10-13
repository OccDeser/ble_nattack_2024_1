/*
 * @Author       : YongkangXiao xiaoyongkang@whu.edu.cn
 * @Date         : 2024-05-12 16:24:39
 * @LastEditTime : 2024-05-12 16:52:08
 * @FilePath     : /type-tamarin/include/log.h
 * @Description  :
 * @Encoding     : UTF-8
 */

#ifndef LOG_H
#define LOG_H

#define LOG_BUFFER_SIZE 1024

typedef enum {
    Error,
    Warning,
    Debug,
} LogType;

void logging(LogType type, const char* format, ...);

#define ERROR(format, ...) logging(Error, format, ##__VA_ARGS__)
#define WARNING(format, ...) logging(Warning, format, ##__VA_ARGS__)
#define DEBUG(format, ...) logging(Debug, format, ##__VA_ARGS__)

#endif
