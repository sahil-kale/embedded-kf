// test/main.cpp
#include "CppUTest/CommandLineTestRunner.h"

IMPORT_TEST_GROUP(dummy_test);
IMPORT_TEST_GROUP(kalman_api_test);
IMPORT_TEST_GROUP(kalman_predict_test);
IMPORT_TEST_GROUP(kalman_update_test);

int main(int ac, char **av) { return CommandLineTestRunner::RunAllTests(ac, av); }